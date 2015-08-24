from py2neo.server import GraphServer

# Script to retrieve from the db 1000 sentence of each type
# Sentences are stored in file txt
def getSentencesByType():

	server = GraphServer("../../neo4j")
	server.start()
	graph=server.graph

	affirmativeSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='affirmative' RETURN n LIMIT 1000")
	exclamationSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='exclamation' RETURN n LIMIT 1000")
	interrogativeSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='interrogative' RETURN n LIMIT 1000")
	
	positiveSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='positive' RETURN n LIMIT 1000")
	negativeSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='negative' RETURN n LIMIT 1000")
	server.stop()

	f = open('affirmative.txt', 'w')
	for affirmativeSentence in affirmativeSentences:
		f.write(affirmativeSentence[0].properties["full_sentence"].encode('utf-8')+'\n')
	f.close()

	f = open('exclamation.txt', 'w')
	for exclamationSentence in exclamationSentences:
		f.write(exclamationSentence[0].properties["full_sentence"].encode('utf-8')+'\n')
	f.close()

	f = open('interrogative.txt', 'w')
	for interrogativeSentence in interrogativeSentences:
		f.write(interrogativeSentence[0].properties["full_sentence"].encode('utf-8')+'\n')
	f.close()

	f = open('positive.txt', 'w')
	for positiveSentence in positiveSentences:
		f.write(positiveSentence[0].properties["full_sentence"].encode('utf-8')+'\n')
	f.close()

	f = open('negative.txt', 'w')
	for negativeSentence in negativeSentences:
		f.write(negativeSentence[0].properties["full_sentence"].encode('utf-8')+'\n')
	f.close()


getSentencesByType()