from py2neo import Node, Relationship
from py2neo.server import GraphServer

def initStatsGraph(graph):

	stats = Node("Stats", label="Stats")
	graph.create(stats)

	greet = Node("SentenceStat", label="greetings")
	has = Relationship(stats, 'has', greet)
	graph.create(has)

	intNeg = Node("SentenceStat", label="interrogative negative")
	has = Relationship(stats, 'has', intNeg)
	graph.create(has)

	intPos = Node("SentenceStat", label="interrogative positive")
	has = Relationship(stats, 'has', intPos)
	graph.create(has)

	exNeg = Node("SentenceStat", label="exclamation negative")
	has = Relationship(stats, 'has', exNeg)
	graph.create(has)

	exPos = Node("SentenceStat", label="exclamation positive")
	has = Relationship(stats, 'has', exPos)
	graph.create(has)

	affNeg = Node("SentenceStat", label="affirmative negative")
	has = Relationship(stats, 'has', affNeg)
	graph.create(has)

	affPos = Node("SentenceStat", label="affirmative positive")
	has = Relationship(stats, 'has', affPos)
	graph.create(has)

def buildStats(graph):

	for typeOfSentence in graph.find("SentenceStat"):

		print typeOfSentence
		if(typeOfSentence.properties["label"] == "greetings"):
			typeSentence = graph.cypher.execute("MATCH (:SentenceType{label:'affirmative'})<--(:Sentence)<--(:Dialogue)<--(n:Sentence) RETURN n")
			print typeSentence
		# else:
		# str1 = typeOfSentence
		# str2 = typeOfSentence
		# sentences = graph.cypher.execute('MATCH (n:)-[:is_of_type{label:""}]-() WHERE n. RETURN n')


server = GraphServer("../../neo4j")
graph=server.graph
buildStats(graph)
