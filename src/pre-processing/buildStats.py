from py2neo import Node, Relationship
from py2neo.server import GraphServer
from collections import defaultdict

def initStatsGraph(graph):

	stats = Node("Stats", label="Stats")
	graph.create(stats)

	greet = Node("TypeStat", label="greeting")
	has = Relationship(stats, 'has', greet)
	graph.create(has)

	intNeg = Node("TypeStat", label="interrogative negative")
	has = Relationship(stats, 'has', intNeg)
	graph.create(has)

	intPos = Node("TypeStat", label="interrogative positive")
	has = Relationship(stats, 'has', intPos)
	graph.create(has)

	exNeg = Node("TypeStat", label="exclamation negative")
	has = Relationship(stats, 'has', exNeg)
	graph.create(has)

	exPos = Node("TypeStat", label="exclamation positive")
	has = Relationship(stats, 'has', exPos)
	graph.create(has)

	affNeg = Node("TypeStat", label="affirmative negative")
	has = Relationship(stats, 'has', affNeg)
	graph.create(has)

	affPos = Node("TypeStat", label="affirmative positive")
	has = Relationship(stats, 'has', affPos)
	graph.create(has)

# Take a dictionaire with number of occurence of each sentene types
# Return dictionaire with probas of each sentene type 
def computeProbs(occurences):

	probas = dict();

	total_sentence = 0.0
	for typeOcc in occurences:
		total_sentence = total_sentence + occurences[typeOcc]
	
	for typeOcc in occurences:
		probas[typeOcc] = occurences[typeOcc]/total_sentence

	return probas

def buildQuery(typesNodePath):

	queryString = "MATCH (d:Dialogue)"
	typeString = ""
	for key, node in enumerate(typesNodePath):
		queryString = queryString + "-->(s"+str(key)+":Sentence)"
		if node.properties['label'] == "greeting":
			typeString = typeString + ", (s"+str(key)+":Sentence)--(:SentenceType{label:'"+node.properties['label']+"'})"
		else:
			typeString = typeString + ", (s"+str(key)+":Sentence)--(:SentenceType{label:'"+node.properties['label'].rsplit()[0]+"'}), (s"+str(key)+":Sentence)--(:SentenceType{label:'"+node.properties['label'].rsplit()[1]+"'})"
	queryString = queryString+"-->(s"+str(len(typesNodePath))+":Sentence)" + typeString + " RETURN s"+str(len(typesNodePath))

	return queryString

def buildProb(graph, typesNodePath):

	occurences = dict();

	queryString = buildQuery(typesNodePath)
	sentences = graph.cypher.execute(queryString)

	for sentence in sentences:

		types = graph.cypher.execute("MATCH (s:Sentence{id:'"+sentence[0].properties['id']+"'})--(t:SentenceType) RETURN t")
		if types[0][0].properties['label']+" "+types[1][0].properties['label'] in occurences:
			occurences[types[0][0].properties['label']+" "+types[1][0].properties['label']] = occurences[types[0][0].properties['label']+" "+types[1][0].properties['label']]+1
		else:
			occurences[types[0][0].properties['label']+" "+types[1][0].properties['label']] = 1

	probas = computeProbs(occurences)
	next = len(probas)

	followingsNode = []
	for key, sType in enumerate(probas):
		typeProbNode = Node("TypeStat", label=sType, prob=probas[sType])
		has = Relationship(typesNodePath[-1], 'has', typeProbNode)
		graph.create(has)
		followingsNode.append(typeProbNode)
		
	if len(typesNodePath) < 5 and next != 0:
		for node in followingsNode:
			typesNodePath.append(node)
			buildProb(graph, typesNodePath)
			typesNodePath.pop()

def buildStats(graph):

	typesNode = graph.find("TypeStat")
	# For each type build its path with associated probs
	for typeNode in typesNode:

		buildProb(graph, [typeNode])