import numpy as np
import json
import os

data = []

for file in os.listdir('datasets'):
	for line in open('datasets/' + file):
		data.append(json.loads(line))


print(len(data))