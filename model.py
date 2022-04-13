import gzip
import os
import json
from tkinter import W
import pandas as pd
from tqdm import tqdm
import plotly.express as px
import numpy as np
from sklearn import preprocessing
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score
import shutil
from processDataset import *
from datetime import datetime
from sklearn.model_selection import train_test_split
import pickle

from processDataset import *
from sim_helpers import *

output_dir = 'output'

def trainModel(user_num):
	user_summary = get_user_summary(output_dir)
	sorted_users_by_event = {k:v for k,v in sorted(user_summary.items(), key=lambda item: item[1]['event_count'], reverse=True)}
	data = get_user_data(list(sorted_users_by_event.keys())[user_num], output_dir)
	
	X, y = get_X_y(data, 50)

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=42)
	print("uuid: " + str(data[0]['uuid']))
	print(f"Total train size : {len(X_train)}")
	print(f"Total test size : {len(X_test)}")

	regr = MultiOutputRegressor(Ridge(random_state=123)).fit(X_train.values, y_train.values)

	preds = pred_to_df(regr.predict(X_test.values).round(), y_test.columns)

	print(f"Accuracy is : {accuracy_score(preds, y_test)*100}%")

	path = 'models/' + str(data[0]['uuid']) + '.pickle'
	file = open(path, 'wb')
	pickle.dump(regr, file)

	
def loadModel(uuid):
	path = 'models/' + str(uuid) + '.pickle'
	file = open(path, 'rb')
	regr = pickle.load(file)
	return regr

trainModel(0)