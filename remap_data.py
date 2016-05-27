from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.marvel

count = 0
spider_man = ['spiderman', 'spider man']
iron_man = ['tonystarks', 'tony starks', 'iron man', 'ironman']
captain_america = ['captainamerica', 'captain', 'captain america']

  