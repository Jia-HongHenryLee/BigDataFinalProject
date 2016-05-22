from pymongo import MongoClient
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import json

class MyListener(StreamListener):
 
	def on_data(self, data):
		try:
			json_data = json.loads(data)
			client = MongoClient('localhost:27017')
			db = client.marvel
			db.raw_data.insert(json_data)
			print('go')
			return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True
 
	def on_error(self, status):
		print(status)
		return True


consumer_key = 'k0PpHIjzWfqAck4bUmB8SIsuH'
consumer_secret = 'beZCriTYp9PO6JIQlhbywolW9TaKCuKaieMFUUOY8pf2IxC7oB'
access_token = '709696570376097792-iBG4pPlLGKZ3CeNq5HVyKIy3btwHGCM'
access_secret = 'I971yZYdGKsL1TZ49Tv0GdSgX5MopvcguXN8ltyga31Rg'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True,
				 wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5,
                 retry_errors=set([401, 404,420, 500, 503]))
count = 0

# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=['#marvel'])
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


while True:
	
	for data in limit_handled(tweepy.Cursor(api.search, q="marvel", rpp=100, include_entities=True, lang="en").items()):
		json_data = data
		try:
			client = MongoClient('localhost:27017')
			db = client.marvel
			print(json_data._json)
			db.raw_data.insert(json_data._json)
			count = count + 1
			print(count)
		except BaseException as e:
			print("Error on_data: %s" % str(e))