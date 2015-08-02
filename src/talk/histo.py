import nltk;
import sys;
import db;

def getTokensAndType(sentence):
	allTokens = nltk.word_tokenize(sentence)
	tagged = nltk.pos_tag(allTokens)
	tokens = []
	for tag in tagged:
		if tag[1].startswith('NN') or tag[1].startswith('VB'):
			tokens.append(tag[0])

	sentenceType = []
	if '?' == allTokens[-1]:
		sentenceType.append('interrogative')
	elif '!' == allTokens[-1]:
		sentenceType.append('exclamation')
	else:
		sentenceType.append('affirmative')

	if "n't" in allTokens:
		sentenceType.append('negative')
	else:
		sentenceType.append('positive')

	greetingsWords = ['Hi', 'hi', 'HI' ,'Hello','hello', 'HELLO','Hey', 'hey', 'HEY','Good morning', 'good morning', 'GOOD MORNING', 'Good afternoon', 'good afternoon', 'GOOD AFTERNOON', 'Good evening', 'good evening', 'GOOD EVENING']
	greet = [val for val in allTokens if val in greetingsWords]
	if greet:
		sentenceType.append('greeting')

	return tokens, sentenceType;