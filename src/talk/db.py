from py2neo.server import GraphServer
from py2neo import Node,Relationship

HISTO_LENGTH = 5

def insert(sentence, tokensAndType):

	server = GraphServer("../../../neo4j")
	graph=server.graph

	sentences = list(graph.find("SentenceHisto"))
	numberOfSentences = len(sentences)

	sentence = Node("SentenceHisto", sentence=sentence)
	sentenceType = graph.find_one("SentenceType",
                    property_key="label",
                    property_value = tokensAndType[1][0])

	sentenceForm = graph.find_one("SentenceType",
                    property_key="label",
                    property_value = tokensAndType[1][1])
	is_of_type = Relationship(sentence, "is_of_type", sentenceType)
	is_of_form = Relationship(sentence, "is_of_type", sentenceForm) # pos / neg
	graph.create(is_of_type)
	graph.create(is_of_form)

	print numberOfSentences
	if numberOfSentences == 0:
		histo = graph.find_one("Histo",
								property_key="label",
								property_value = "histo")
		has = Relationship(histo, "is_followed_by", sentence)
		graph.create(has)
	elif numberOfSentences == HISTO_LENGTH:
		histo = graph.find_one("Histo",
								property_key="label",
								property_value = "histo")
		has = Relationship(histo, "is_followed_by", sentences[1])
		graph.create(has)

		graph.cypher.execute("MATCH (n:SentenceHisto)-[r]-() WHERE n.sentence=\""+sentences[0]["sentence"]+"\" DELETE n, r")
		is_followed_by = Relationship(sentences[-1], "is_followed_by", sentence)
		graph.create(is_followed_by)

	else:
		is_followed_by = Relationship(sentences[-1], "is_followed_by", sentence)
		graph.create(is_followed_by)
		
	for token in tokensAndType[0]:
		tokenNode = graph.find_one("Token",
							   property_key="token",
							   property_value = token)
		if tokenNode is None:
			tokenNode = Node("Token", token=token)
		
		is_composed_of = Relationship(sentence, "is_composed_of", tokenNode)
		graph.create(is_composed_of)
