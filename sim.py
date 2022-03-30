from email.mime import application
import json
import ast

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
			
		
class Event:
	def __init__(self, type, location, time, app):
		self.type = type
		self.location = location
		self.time = time
		self.app = app

class sim:
	def __init__(self, input, RAM, location, time):
		self.input = input
		self.device = Device(RAM, location, time)

	def runInput(self):
		for event in self.input:
			self.device.processEvent(event)

f = open('top10users.txt', 'r')
users = {}
for line in f:
	items = line.split('~')
	users[items[0]] = []
	events = ast.literal_eval(items[1])
	for e in events:
		e = str(e).replace('\'', '\"')
		users[items[0]].append(json.loads(e))


for u in users:
	print(u)
	print(len(users[u]))

app_list = set()
for u in users:
	for e in users[u]:
		for app in e['apps']:
			if app['processName'] not in app_list:
				app_list.add(app['processName'])

print(app_list)
print(len(app_list))