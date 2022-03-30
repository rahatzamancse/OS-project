import numpy as np
import json
import os

data = []
users = {}
unimportant_fields = ['timeZone', 'mobileCountryCode', 'batteryStatus']

i = 0
for file in os.listdir('datasets'):
	i += 1
	if i % 10 == 0:
		print(i)
	if i > 400:
		break
	for line in open('datasets/' + file):
		event = json.loads(line)
		event['apps'] = [app for app in event['apps'] if app['priority'] == 'Foreground app']

		for field in unimportant_fields:
			del event[field]
	
		uuid = event['uuid']
		del event['uuid']

		# if uuid in users.keys():
		# 	users[uuid].append(event)
		# else:
		# 	users[uuid] = [event]
		data.append(event)
		
print(len(users))