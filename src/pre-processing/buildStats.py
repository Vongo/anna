from py2neo.server import GraphServer

def initStatsGraph(graph):

	stats = Node("Stats", label="Stats")
	graph.create(stats)

	has = Relationship()

	greet = Node("SentenceStat", label="greetings")
	has = Relationship(stats, 'has', stats)
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

# def buildStats(graph):

# 	for typeOfSentence in graph.find("SentenceStat"):

# 		sentences = graph.cypher.execute('MATCH -[r]-(n:Sentence)')


# 	pour chaque type de phrases retirer les phrases suivantes
# 		attibuer proba à chaque type de phrase
# 		insérer en base
		
server = GraphServer("../../../neo4j")
graph=server.graph
initStatsGraph(graph)
