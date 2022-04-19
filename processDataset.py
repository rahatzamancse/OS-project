import gzip
import os
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import heapq
import plotly.express as px

import numpy as np
from sklearn import preprocessing

from processDataset import *


def previous():
    data = []
    users = {}
    unimportant_fields = ['timeZone', 'mobileCountryCode']

    i = 0
    for file in os.listdir('datasets'):
        i += 1
        if i % 10 == 0:
            print(i)
        if i > 100:
            break
        for line in open('datasets/' + file):
            event = json.loads(line)
            event['apps'] = [app['processName'] for app in event['apps'] if app['priority'] == 'Foreground app']

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

def preprocess_dataset(DATA_DIR, output_dir):
    data = []
    unimportant_fields = ['timeZone', 'mobileCountryCode']

    files = {}

    for file in tqdm(os.listdir(os.path.join(DATA_DIR))):
        if not file.endswith('gz'):
            continue
        file = DATA_DIR + file
        with gzip.open(file) as f:
            for line in f.readlines():
                json_data = json.loads(line)
                for unimportant_field in unimportant_fields:
                    del json_data[unimportant_field]
                json_data['apps'] = [app['processName'] for app in json_data['apps'] if app['priority'] == 'Foreground app']

                file = os.path.join(output_dir, json_data['uuid'] + ".txt")
                if file not in files:
                    files[file] = open(file, 'a')
                files[file].write(json.dumps(json_data) + "\n")

    for file_name, file in files.items():
        file.close()
    

def get_user_summary(preprocessed_dir):
    user_summary = {}

    for file in tqdm(os.listdir(preprocessed_dir)):
        with open(os.path.join(preprocessed_dir, file), 'r') as f:
            for line in f.readlines():
                json_data = json.loads(line)
                if json_data['uuid'] not in user_summary:
                    user_summary[json_data['uuid']] = {
                        'event_count': 0,
                        'unique_apps': set()
                    }
                user_summary[json_data['uuid']]['event_count'] += 1
                user_summary[json_data['uuid']]['unique_apps'] |= set(json_data['apps'])

    print(f"Total users : {len(user_summary)}")
    return user_summary

def pred_to_df(pred, cols):
    return pd.DataFrame(pred, columns=cols, dtype=int)

def get_user_data(uuid, output_dir):
    data = []

    with open(os.path.join(output_dir,uuid+'.txt'), 'r') as f:
        for line in f.readlines():
            json_data = json.loads(line)
            data.append(json_data)
            
    return data

def get_app_freq(data):
    app_freq = {}

    for datum in data:
        for app in datum['apps']:
            if app not in app_freq:
                app_freq[app] = 0
            app_freq[app] += 1
    return app_freq




def get_X_y(data, top_n_apps=50):
    app_freq = get_app_freq(data)
    top_50_freq_apps = [k for k,v in sorted(app_freq.items(), key=lambda item: item[1], reverse=True)][:top_n_apps]
    processedData = []

    for datum in tqdm(data):
        processedDatum = {
            'batteryLevel': datum['batteryLevel'],
            'batteryStatus': datum['batteryStatus'],
            'timestamp': datum['timestamp'],
        }
        for selectedApp in top_50_freq_apps:
            if selectedApp in datum['apps']:
                processedDatum[selectedApp] = 1
            else:
                processedDatum[selectedApp] = 0

        processedData.append(processedDatum)
    
    X_tmp = pd.DataFrame(processedData)
    X_tmp = X_tmp.dropna(axis=1)
    
    battery_status_encoder = preprocessing.LabelEncoder()
    X_tmp['batteryStatus'] = battery_status_encoder.fit_transform(X_tmp['batteryStatus'])

    battery_level_scaler = preprocessing.MinMaxScaler()
    X_tmp['batteryLevel'] = battery_level_scaler.fit_transform(X_tmp['batteryLevel'].values.reshape(-1, 1))
    
    X_tmp = X_tmp.sort_values(by=['timestamp']).reset_index().drop(['index'], axis=1)
    
    def get_secs_from_time(t):
        t = str(datetime.utcfromtimestamp(t).time())[:5]
        secs = int(t[:2]) * 60 + int(t[3:])
        return secs
    X_tmp['timestamp'] = X_tmp['timestamp'].apply(get_secs_from_time)
    
    timestamp_scaler = preprocessing.MinMaxScaler()
    X_tmp['timestamp'] = timestamp_scaler.fit_transform(X_tmp['timestamp'].values.reshape(-1, 1))
    
    y = X_tmp.iloc[:, 3:].copy()
    y = y.drop(y.index[0]).reset_index().drop(['index'], axis=1)
    
    X_tmp = X_tmp.drop(X_tmp.index[-1]).reset_index().drop(['index'], axis=1)
    
    return X_tmp, y
