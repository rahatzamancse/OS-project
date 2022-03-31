import numpy as np
import json
import os
import heapq

data = []
users = {}
unimportant_fields = ['timeZone', 'mobileCountryCode', 'batteryStatus']

i = 0
for file in os.listdir('datasets'):
	i += 1
	if i % 10 == 0:
		print(i)
	if i > 100:
		break
	for line in open('datasets/' + file):
		event = json.loads(line)
		event['apps'] = [app for app in event['apps'] if app['priority'] == 'Foreground app']

		for field in unimportant_fields:
			del event[field]
	
		uuid = event['uuid']
		del event['uuid']

		if uuid in users.keys():
			users[uuid].append(event)
		else:
			users[uuid] = [event]
		data.append(event)
		
print(len(users))

max_users = heapq.nlargest(10, users.items(), key=lambda i: len(i[1]))

out_file = ''
for user in max_users:
	out_file += user[0] + '~' + json.dumps(user[1]) + '\n'

out = open('top10users.txt', 'w')
out.write(out_file)
out.close()


# min_len = -1
# max_len = 0
# mean_len = 0
# for u in users:
# 	amt = len(users[u])
# 	if min_len == -1 or amt < min_len:
# 		min_len = amt
# 	if amt > max_len:
# 		max_len = amt

# 	mean_len += amt

# mean_len = float(mean_len) / float(len(users))

# print(min_len)
# print(max_len)
# print(mean_len)