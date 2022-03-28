
class Device:
	def __init__(self, RAM, location, time) -> None:
		battery = 100.0
		self.RAM = RAM
		self.location = location
		self.time = time
		self.app_to_ram = {}
		
	def processEvent(event):
		pass
		
class Event:
	def __init__(self, type, location, time, app):
		self.type = type
		self.location = location
		self.time = time
		self.app = app

class sim:
	def __init__(self, input, RAM, location, time) -> None:
		self.input = input
		self.device = Device(RAM, location, time)

	def runInput(self):
		for event in self.input:
			self.device.processEvent(event)