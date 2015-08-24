import nltk;
import sys;
import db;

# Take a sentence and return relevant tokens, the type of the sentence  
# and proper names
def getTokensAndType(sentence):

	allTokens = nltk.word_tokenize(sentence) # tokenize the sentence
	tagged = nltk.pos_tag(allTokens) # Tag the tokens


	tokens = []
	nnp = []
	for key, tag in enumerate(tagged):
		# We identify the proper names to be returned
		if tag[1].startswith('NNP'):
			if tagged[key-1][0] != '!' and tagged[key-1][0] != '.' and tagged[key-1][0] != '?' and key != 0:
				nnp.append(tag[0])
		# We identify the relevant tokens to be returned
		elif tag[1].startswith('NN') or tag[1].startswith('VB') or tag[1].startswith('PRP') or tag[0] == "that":
			tokens.append([tag[0], tag[1]])

	# We identify the type of the sentence
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
	# if the sentence contains one of the following keywords then its type is greeting
	greetingsWords = ['Hi', 'hi', 'HI' ,'Hello','hello', 'HELLO','Hey', 'hey', 'HEY','Good morning', 'good morning', 'GOOD MORNING', 'Good afternoon', 'good afternoon', 'GOOD AFTERNOON', 'Good evening', 'good evening', 'GOOD EVENING']
	greet = [val for val in allTokens if val in greetingsWords]
	if greet:
		sentenceType.append('greeting')

	return tokens, sentenceType, nnp;