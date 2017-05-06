import pickle
import nltk

classifier = pickle.load(open('data/trained/MNB.pickle', 'rb'))
word_features = pickle.load(open('data/trained/word_features.pickle', 'rb'))

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

def predict_topic(s):
	token = nltk.word_tokenize(s.lower())
	return classifier.classify(document_features(token))



topic = predict_topic("""Well, that is taxation law of India (other side).In India 52,911 
						Profitable Companies Pay 0% Tax in India!""")

print(topic)