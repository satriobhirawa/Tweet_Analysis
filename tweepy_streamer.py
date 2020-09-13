import twitter as twitter
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
#class that will be responsible for actually streaming the tweets
class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    #unlike the function before (only printing the tweets)
    #we can now save as text, JSON or whatever
    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        #this handles twitter authentication and the connection to the twitter streaming API.
        # listener obj responsible with how the deal data and tweets, errors
        listener = StdOutListener()
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        # filter the tweet
        stream.filter(track=hash_tag_list)

#inherit from StreamListener
class StdOutListener(StreamListener):
    """
    This a basic listener class that just prints received tweets to stdout
    """
    #standard class
    def init (self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    #file name or where do we want to save the tweets
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    #take data that streamed in on tweets
    #we can do whatever we want with the data
    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    #passes the error
    def on_error(self, status):
        print(status)

#object from StdOutListener class stream it to this
if  __name__  == "__main__":
    hash_tag_list = ["PSBB","COVID19INDONESIA","Indonesia"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)