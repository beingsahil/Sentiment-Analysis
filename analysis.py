import re
import tweepy
from tweepy import OAuthHandler
import matplotlib.pyplot as plt
from textblob import TextBlob
class TwitterClient(object):


    def __init__(self):

        consumer_key = 'QiI95tqgBqUFyyvtqE6kvQ0iw'
        consumer_secret = 'hUjtmafuPKOQuycRqISCvYqcO1b2slA3GT3Xvv0LcUyeMI5cbc'
        access_token = '973792918153637888-TtcX4Qr7EZxYgmhDrUU0bLLn0aoYwrs'
        access_token_secret = 'uEJvqV1C4LUa2o3QQ4YFYOZeIm18LjQRb51RlRjbt0IFs'


        try:

            self.auth = OAuthHandler(consumer_key, consumer_secret)

            self.auth.set_access_token(access_token, access_token_secret)

            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):

        tweets = []

        try:

            fetched_tweets = self.api.search(q=query, count=count)


            for tweet in fetched_tweets:

                parsed_tweet = {}


                parsed_tweet['text'] = tweet.text

                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)


                if tweet.retweet_count > 0:

                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)


            return tweets

        except tweepy.TweepError as e:

            print("Error : " + str(e))

a = input("enter the query to be searched:-")
b=input("enter no of tweets to be searched:-")

def plotPieChart(x, y, z, b):
    labels = ['Positive [' + str(x) + '%]', 'Negative [' + str(y) + '%]', 'Neutral [' + str(z) + '%]']
    sizes = [x, y, z]
    colors = ['red', 'c', 'blue']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90,explode=(0,0.1,0.05))
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + a + 'by analyzing ' + str(b) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    pass

def main():

    api = TwitterClient()


    tweets = api.get_tweets(query=a, count=b)


    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    x=100 * len(ptweets)/len(tweets)


    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    y=100 * len(ntweets)/len(tweets)

    print("neutral tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
    z=100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])


    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
    plotPieChart(x, y, z, b)


if __name__ == "__main__":

    main()