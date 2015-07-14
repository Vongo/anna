from py2neo.server import GraphServer

def getSentencesByType():

	server = GraphServer("../../neo4j")
	server.start()
	graph=server.graph

	affirmativeSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='affirmative' RETURN n LIMIT 25")
	exclamationSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='exclamation' RETURN n LIMIT 25")
	interrogativeSentences = graph.cypher.execute("MATCH (n:Sentence)-->(t:SentenceType) WHERE t.label='interrogative' RETURN n LIMIT 25")
	
	server.stop()

	f = open('affirmative.txt', 'w')
	for affirmativeSentence in affirmativeSentences:
		f.write(affirmativeSentence[0].properties["full_sentence"]+'\n')
	f.close()

	f = open('exclamation.txt', 'w')
	for exclamationSentence in exclamationSentences:
		f.write(exclamationSentence[0].properties["full_sentence"]+'\n')
	f.close()

	f = open('interrogative.txt', 'w')
	for interrogativeSentence in interrogativeSentences:
		f.write(interrogativeSentence[0].properties["full_sentence"]+'\n')
	f.close()



getSentencesByType()