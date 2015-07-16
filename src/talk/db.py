from py2neo.server import GraphServer
from py2neo import Node,Relationship

HISTO_LENGTH = 5

def insert(sentence, tokensAndType):
	server = GraphServer("../../../neo4j")
	
	graph=server.graph

	sentences = list(graph.find("Sentence"))
	numberOfSentences = len(sentences)

	sentence = Node("Sentence", sentence=sentence)
	sentenceType = Node("Type", type=tokensAndType[1][0], form=tokensAndType[1][1])
	is_of_type = Relationship(sentence, "is_of_type", sentenceType)
	graph.create(is_of_type)

	print numberOfSentences
	if numberOfSentences == 0:
		histo = graph.find_one("Histo",
								property_key="label",
								property_value = "histo")
		has = Relationship(histo, "has", sentence)
		graph.create(has)
	elif numberOfSentences == HISTO_LENGTH:

		histo = graph.find_one("Histo",
								property_key="label",
								property_value = "histo")
		has = Relationship(histo, "has", sentences[1])
		graph.create(has)

		graph.cypher.execute("MATCH (n:Sentence)-[r]-() WHERE n.sentence=\""+sentences[0]["sentence"]+"\" DELETE n, r")
		is_followed_by = Relationship(sentences[-1], "is_followed_by", sentence)
		graph.create(is_followed_by)

	else:
		is_followed_by = Relationship(sentences[-1], "is_followed_by", sentence)
		graph.create(is_followed_by)
		

	for token in tokensAndType[0]:
		token = Node("Token", token=token)
		is_composed_of = Relationship(sentence, "is_composed_of", token)
		graph.create(is_composed_of)

	server.stop()
	print "fin db"