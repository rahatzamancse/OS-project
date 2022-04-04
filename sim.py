import json
import ast

# The device class manages all the devices resources such as battery, RAM, etc
class Device:
	def __init__(self, RAM, location, time) -> None:
		battery = 100.0
		self.RAM = RAM
		self.location = location
		self.time = time
		self.app_to_ram = {}
		self.name_to_app = {}
		self.warm_apps = []
		self.cold_apps = []
		self.hot_apps = []
		
	def processEvent(event):
		pass

class Application:
	def __init__(self, name, mem_use):
		self.name = name
		self.mem_use = mem_use
			
# This is the Event class. It classifies events from the input as a object, with the location, time, and app opened during this time.
class Event:
	def __init__(self, type, location, time, app):
		self.type = type
		self.location = location
		self.time = time
		self.app = app

# First, create the sim with the input, desired RAM and the starting location and time.
# The sim will create the device with the desired attributes and run the input
class Sim:
	def __init__(self, input, RAM, location, time):
		self.input = input
		self.device = Device(RAM, location, time)

	def runInput(self):
		for event in self.input:
			self.device.processEvent(event)

print('Loading Dataset ...')
f = open('top10users.txt', 'r')
users = {}
lineNum = 0
for line in f:
    lineNum += 1
    print(lineNum)
    items = line.split('~')
    users[items[0]] = []
    events = ast.literal_eval(items[1])
    for e in events:
        e = str(e).replace('\'', '\"')
        users[items[0]].append(json.loads(e))

for u in users:
	print(u)
	print(len(users[u]))

print('Fetching Applications ...')
app_list = set()
for u in users:
	for e in users[u]:
		for app in e['apps']:
			if app['processName'] not in app_list:
				app_list.add(app['processName'])

print('Sorting Events by TimeStamp ...')
for u in users:
    u = sorted(u, key=lambda x: x['timestamp'])
    for event in u:
        print(event['timestamp'])
    break


print(app_list)
print(len(app_list))

applications = set()

for app in app_list:
    application = Application(app, 200)
    applications.add(application)

