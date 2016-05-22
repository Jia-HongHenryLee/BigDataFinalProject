from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
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
 
api = tweepy.API(auth)

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])