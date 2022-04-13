from email.mime import application

from zmq import device
from sim_helpers import *
from processDataset import *
from datetime import datetime
from model import *
import sys

# The device class manages all the devices resources such as battery, RAM, etc
class Device:
    def __init__(self, RAM, location, time) -> None:
        battery = 100.0
        self.RAM = RAM
        self.RAM_cap = 500
        self.RAM_reset = 150
        self.total_RAM = RAM
        self.location = location
        self.time = time
        self.applications = []
        self.down_time = 0.0
        self.current_date = None
        self.total_dates = 0
        self.avg_start_RAM = 0

    def processEvent(self, event):
        self.time = event['timestamp']
        dt = datetime.utcfromtimestamp(self.time)

        last_date = self.current_date
        self.current_date = dt.day

        if last_date != self.current_date:
            for app in self.applications:
                if categories_to_RAM[app_to_category[app]] > self.RAM_reset:
                    self.applications.pop(self.applications.index(app))
                    self.RAM += categories_to_RAM[app_to_category[app]]
            self.avg_start_RAM += self.RAM
            # self.applications = []
            # self.RAM = self.total_RAM
            self.total_dates += 1

        # print('current RAM: ' + str(self.RAM))
        # Go through foreground apps and add them to RAM
        for app in event['apps']:
            if app not in self.applications:
                # If there is NOT enough RAM for this application
                if app not in app_to_category:
                    app_to_category[app] = 'OTHER'
                while self.RAM < categories_to_RAM[app_to_category[app]]:

                    top_RAM_use = 0
                    top_idx = 0
                    i = 0
                    for ram_app in self.applications:
                        if categories_to_RAM[app_to_category[ram_app]] > top_RAM_use:
                            top_RAM_use = categories_to_RAM[app_to_category[ram_app]]
                            top_idx = i
                        i += 1
                    if top_RAM_use >= self.RAM_cap:
                        evicted = self.applications.pop(top_idx)
                    else:
                        evicted = self.applications.pop(0)
                    self.RAM += categories_to_RAM[app_to_category[evicted]]

                self.RAM -= categories_to_RAM[app_to_category[app]]
                self.down_time += max(categories_to_RAM[app_to_category[app]] / float(90), 5.0)
            else:
                self.applications.remove(app)
                self.down_time += 0

            # Add app to the top of the stack
            self.applications.append(app)


# First, create the sim with the input, desired RAM and the starting location and time.
# The sim will create the device with the desired attributes and run the input
class Sim:
    def __init__(self, input, RAM):
        self.model = loadModel(input[0]['uuid'])
        self.input = sorted(input, key=lambda x: int(x['timestamp']))
        location = None
        time = self.input[0]['timestamp']
        self.device = Device(RAM, location, time)
        self.prefetched = 0
        self.failed_prefetch = 0
        self.pre_evict = 0

    def runInput(self):
        for event in tqdm(self.input):
            eventTime = get_secs_from_time(event['timestamp'])
            deviceTime = get_secs_from_time(self.device.time)
            
            predicting = True
            while deviceTime + 20 < eventTime and predicting:
                x = prep_input(event, template)
                y_hat = modelPredict(self.model, [x])[0]
                for i in range(0, len(y_hat)):
                    app = template[i + 3]
                    if app not in app_to_category:
                        app_to_category[app] = 'OTHER'
                    if app in self.device.applications and y_hat[i] == 0:
                        self.device.applications.remove(app)
                        self.device.RAM += categories_to_RAM[app_to_category[app]]
                        self.pre_evict += 1
                for i in range(0, len(y_hat)):
                    app = template[i + 3]
                    if app not in self.device.applications and y_hat[i] == 1:
                        if self.device.RAM >= categories_to_RAM[app_to_category[app]]:
                            self.device.applications.insert(0, app)
                            self.device.RAM -= categories_to_RAM[app_to_category[app]]

                            self.prefetched += 1                            
                        else:
                            self.failed_prefetch += 1                            
                deviceTime += 20

            self.device.processEvent(event)


print('Loading Dataset ...')
# user_summary = get_user_summary(output_dir)
# sorted_users_by_event = {k:v for k,v in sorted(user_summary.items(), key=lambda item: item[1]['event_count'], reverse=True)}

# Only get one user for now
# users = []
# for i in range(1):
#     users.append(get_user_data(list(sorted_users_by_event.keys())[i], output_dir))

users = [getData()]

print('Fetching Applications ...')
app_list = get_app_list(users)

app_freq = get_app_freq(users[0])
top_freq_apps = [k for k,v in sorted(app_freq.items(), key=lambda item: item[1], reverse=True)][:50]

template = ['batteryLevel', 'batteryStatus', 'timestamp']
for app in top_freq_apps:
    template.append(app)
    
print('Categorizing Applications ... ')

app_to_category, categories_to_RAM = get_categories()

for u in users:
    print(u[0]['uuid']) 
    init_time = u[0]['timestamp']
    simu = Sim(u, 4096)
    simu.runInput()
    print('total downtime: ' + str(simu.device.down_time))
    average_downtime = simu.device.down_time / float(simu.device.total_dates)
    avg_RAM = simu.device.avg_start_RAM / float(simu.device.total_dates)
    # print('average downtime: ' + str(average_downtime))
    # print()
    print(average_downtime)
    print('total prefetched: ' + str(simu.prefetched))
    print('total pre-evicted: ' + str(simu.pre_evict))
    print('total failed prefetches: ' + str(simu.failed_prefetch))
