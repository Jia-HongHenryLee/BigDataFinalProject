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
    for data in db[collection_name].find():
        # print(data['key'])
        if data['key'] in adjective_list:
        	print(data['key'])

run_and_go('new_ironman', positive_adjetive)
