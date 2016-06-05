import math
import json
from pymongo import MongoClient

with open('positive-words.json') as data_file:
    positive_adjetive = json.load(data_file)

with open('negative-words.json') as data_file:
    negative_adjetive = json.load(data_file)


def run_and_go(collection_name, adjective_list):
    client = MongoClient('localhost:27017')
    db = client.marvel
    adjective_data = []
    max = 0
    for data in db[collection_name].find():
        # print(data['key'])
        if data['key'] in adjective_list:
        	if data['score'] > max:
        		max = data['score']

        	adjective_data.append({'key': data['key'], 'score': data['score']})

    json_data = []
    for data in adjective_data:
    	item = {'text': data['key'], 'size': 20 + 100 * data['score'] / max}    	
    	json_data.append(item)

    with open('./site/' + collection_name + '_adjective.json', 'w') as outfile:
    	json.dump(json_data, outfile)

    print('finished')


run_and_go('new_ironman', positive_adjetive)
