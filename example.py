from twc import Tweetifier


#initialize the object
T = Tweetifier("paraazz", 100)

#crawl or fetch the tweets max: 3200
T.crawl()
crawled_tweets = cur.tweets

#classify the tweets topic wise 
#(Multinomial Naive Bayes Classifier accuracy: 78%)
T.classify()
tweets_topic = T.topic_bucket