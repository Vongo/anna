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

	return tokens, sentenceType;
