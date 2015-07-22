from py2neo import Node, Relationship
from py2neo.server import GraphServer
from collections import defaultdict
from py2neo.packages.httpstream import http

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

# Compute Probability of occurence for each type of sentences
def computeProbs(typesOccurence):

	typesProb = defaultdict(dict)

	for path in typesOccurence:
		total_sentence = 0.0
		for typeOcc in typesOccurence[path]:
			total_sentence = total_sentence + typesOccurence[path][typeOcc]
		
		for typeOcc in typesOccurence[path]:
			typesProb[path][typeOcc] = typesOccurence[path][typeOcc]/total_sentence

	return typesProb

def nodeToStringPath(typesNodePath):

	typesStrPath = ''
	for key, typesNode in enumerate(typesNodePath):

		if key != 0:
			typesStrPath =  typesStrPath +  ' - ' + typesNode.properties['label']
		else:
			typesStrPath = typesStrPath + typesNode.properties['label']

	return typesStrPath

def buildQuery(order, typesNodePath):

	queryString = "MATCH "
	for key, node in enumerate(typesNodePath):
		if node.properties['label'] == "greeting":
			queryString = queryString + "(d:Dialogue)--(s"+str(key)+":Sentence{order:"+str(order)+"}), (s"+str(key)+":Sentence)--(:SentenceType{label:'"+node.properties['label']+"'}), "
		else:
			queryString = queryString + "(d:Dialogue)--(s"+str(key)+":Sentence{order:"+str(order)+"}), (s"+str(key)+":Sentence)--(:SentenceType{label:'"+node.properties['label'].rsplit()[0]+"'}), (s"+str(key)+":Sentence)--(:SentenceType{label:'"+node.properties['label'].rsplit()[1]+"'}), "
		order = order+1
	queryString = queryString+"(d:Dialogue)--(s"+str(len(typesNodePath))+":Sentence{order:"+str(order)+"}) RETURN s"+str(len(typesNodePath))

	return queryString

def buildProb(max_sentence, typesNodePath):

	firstOrder = 0
	typesOccurence = defaultdict(dict)

	for firstOrder in range(0,max_sentence):

		queryString = buildQuery(firstOrder, typesNodePath)
		# print queryString
		sentences = graph.cypher.execute(queryString)
		# print "end query"

		for sentence in sentences:

			resTypes = graph.cypher.execute("MATCH (s:Sentence{id:'"+sentence[0].properties['id']+"'})--(t:SentenceType) RETURN t")
			typeStrPath = nodeToStringPath(typesNodePath)
			if resTypes[0][0].properties['label']+" "+resTypes[1][0].properties['label'] in typesOccurence[typeStrPath]:
				typesOccurence[typeStrPath][resTypes[0][0].properties['label']+" "+resTypes[1][0].properties['label']] = typesOccurence[typeStrPath][resTypes[0][0].properties['label']+" "+resTypes[1][0].properties['label']]+1
			else:
				typesOccurence[typeStrPath][resTypes[0][0].properties['label']+" "+resTypes[1][0].properties['label']] = 1
		firstOrder = firstOrder+1

	typeProbs = computeProbs(typesOccurence)
	print nodeToStringPath(typesNodePath)
	print typeProbs
	print '\r \r'
	next = len(typeProbs)

	typeStrPath = nodeToStringPath(typesNodePath)
	followingsNode = []
	for typeProb in typeProbs[typeStrPath]:
		typeProbNode = Node("TypeStat", label=typeProb, prob=typeProbs[typeStrPath][typeProb])
		has = Relationship(typesNodePath[-1], 'has', typeProbNode)
		# graph.create(has)
		followingsNode.append(typeProbNode)
		
	if len(typesNodePath) < 5 and next != 0:
		for node in followingsNode:
			typesNodePath.append(node)
			buildProb(max_sentence-1, typesNodePath)
			typesNodePath.pop()

def buildStats(graph):

	# Find the max number of sentence in a dialogue
	dialogues = graph.find("Dialogue")
	max_sentence = 0
	for dialogue in dialogues:
		n_sentence = graph.cypher.execute("MATCH (d:Dialogue{id:'"+dialogue.properties["id"]+"'})--(s:Sentence) RETURN count(s)")
		if n_sentence[0]["count(s)"] > max_sentence:
			max_sentence = n_sentence[0]["count(s)"]

	typesNode = graph.find("TypeStat")
	# For each type build its path with associated probs
	for typeNode in typesNode:

		buildProb(max_sentence, [typeNode])


http.socket_timeout = 9999
server = GraphServer("../../neo4j")
graph=server.graph
buildStats(graph)