import nltk;
import sys;
import db;

def getTokensAndType(sentence):

	allTokens = nltk.word_tokenize(sentence)
	tagged = nltk.pos_tag(allTokens)

	tokens = []
	print tagged
	for tag in tagged:
		# print tag
		if tag[1].startswith('NN') or tag[1].startswith('VB'):
			tokens.append(tag[0])

	sentenceType = []
	if '?' in allTokens:
		sentenceType.append('Interrogative')
	elif '!' in allTokens:
		sentenceType.append('Exclamative')
	elif tagged[0] == 'VERB':
		sentenceType.append('Imperative')
	else:
		sentenceType.append('Declarative')

	if 'no' in allTokens or 'not' in allTokens or "don't" in allTokens:
		sentenceType.append('Affirmative')
	else:
		sentenceType.append('Positive')

	return tokens, sentenceType;

sentence = getTokensAndType(sys.argv[1])
print sentence
db.insert(sys.argv[1], sentence)
# nltk.help.upenn_tagset('JJ')