import tweepy
import pickle
import nltk
import re

classifier = pickle.load(open('twc/data/trained/MNB.pickle', 'rb'))
word_features = pickle.load(open('twc/data/trained/word_features.pickle', 'rb'))

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def tweet_clean(t):
		t = t.replace("#", "")
		t = t.replace("@", "")
		t = re.sub(r"[^\w\s]","",t)
		t = re.sub(" \d+", " ", t)
		return t


def is_actionable(t):
	t = tweet_clean(t)
	tags = [i[1] for i in nltk.pos_tag(t.split())]
	if len(t.split())>4:
		if 'NN' and 'VBD' or 'VB' in tags:
			return True
		else:
			False
	else:
		False


def predict_topic(s):
	s = tweet_clean(s)
	token = nltk.word_tokenize(s.lower())
	return classifier.classify(document_features(token))


class Tweetifier:
	def __init__(self, user, count=10):
		self.consumer_key = "8E17QEDQMdi8c2qdEG6bslpdg"
		self.consumer_secret = "Hzrfjmy3e0KyuNEqrGOyUTXrDTKwmes0lWaAmOo7BlqKPHlUWZ"

		self.access_token = "850697540-E6ccBsss0Lx3o1pxlXvRsaXPeWepWTUgvaybR0fq"
		self.access_token_secret = "LgyrN8X0t5ynTcq8NwJ7Atehh0CrD7477wFUKf8NrEolM"

		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token, self.access_token_secret)

		self.count = count
		self.user = user

		self.tweets = []
		self.topic_bucket = {}

	def crawl(self):
		try:
			api = tweepy.API(self.auth)
			for status in tweepy.Cursor(api.user_timeline, id=self.user, retweets=True).items(self.count):
				self.tweets.append(status.text)
		except Exception as e:
			print(e)

	def classify(self):
		for t in self.tweets:
			if is_actionable(t):
				topic = predict_topic(t)
				if self.topic_bucket.get(topic):
					self.topic_bucket[topic].append(t)
				else:
					self.topic_bucket[topic] = [t]


if __name__=="__main__":
	t = Tweetifier("paraazz", count=2)
	t.crawl()
	t.classify()

	print(t.topic_bucket)

	