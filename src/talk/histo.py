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
	if '?' in allTokens:
		sentenceType.append('Interrogative')
	elif '!' in allTokens:
		sentenceType.append('Exclamative')
	else:
		sentenceType.append('Declarative')

	if "n't" in allTokens:
		sentenceType.append('Negative')
	else:
		sentenceType.append('Positive')

	return tokens, sentenceType;