from py2neo import Node, Relationship
from py2neo.server import GraphServer
from collections import defaultdict
import time

# Create and store the fist nodes of the statistic tree
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

def getType(sentence, graph):

	typesNodes = graph.cypher.execute("MATCH (s:Sentence{id:'"+sentence.properties['id']+"'})--(t:SentenceType) RETURN t")

	if len(typesNodes) == 3:
		return 'greeting'
	elif typesNodes[1]['t'].properties['label'] == 'negative' or typesNodes[1]['t'].properties['label'] == 'positive':
		return typesNodes[0]['t'].properties['label'] + ' ' + typesNodes[1]['t'].properties['label']
	else:
		return typesNodes[1]['t'].properties['label'] + ' ' + typesNodes[0]['t'].properties['label']

def computeProbas(occurences):

	probas = defaultdict(lambda: defaultdict(int))

	for sType, typesDico  in occurences.iteritems():

		total_sentence = 0.0
		for s2Type in typesDico:
			total_sentence = total_sentence + typesDico[s2Type]

		for s2Type in typesDico:
			probas[sType][s2Type] = typesDico[s2Type]/total_sentence

	return probas

#
def buildProbas(dialogues, length, graph):

	occurences = defaultdict(lambda: defaultdict(int))
	for key, dialogue in enumerate(dialogues):

			sentences = dialogue['p'].nodes[1:]
			for key, sentence in enumerate(sentences):

				if key>=length:

					previousTypes = ''
					for i in range(0,length):

						if i == 0:
							previousTypes = getType(sentences[key-length+i], graph)
						else:
							previousTypes = previousTypes + ' - ' + getType(sentences[key-length+i], graph)

					currentType = getType(sentence, graph)
					occurences[previousTypes][currentType] = occurences[previousTypes][currentType] + 1

	probas = computeProbas(occurences)

	return probas

def buildQuery(strLabels):

	queryString = "MATCH (:Stats)"
	labels = strLabels.split('-')
	for label in labels:
		if label == labels[-1]:
			queryString = queryString + '--(node:TypeStat{label:"'+label.lstrip().rstrip()+'"})'
		else:
			queryString = queryString + '--(:TypeStat{label:"'+label.lstrip().rstrip()+'"})'

	queryString = queryString + ' RETURN node'

	return queryString

# Insert the statistic tree in the db
def buildTreeStats(probas, graph):

	for key, Dval in probas.iteritems():
		query = buildQuery(key)
		node = graph.cypher.execute(query)

		for v in Dval:
			newNode = Node("TypeStat", label=v, prob=Dval[v])
			has = Relationship(node[0]["node"], 'has', newNode)
			graph.create(has)

# Function called once after the initialisation of the database to build the statistic tree
def buildStats(graph):

	# retrieve all the dialogues in the db
	dialogues = graph.cypher.execute("MATCH p=(d:Dialogue)-[:IS_COMPOSED_OF]-(s1:Sentence{order:0})-[:sentence_followed_by*]-(s:Sentence) WHERE length(p)=toInt(d.n_utterances) RETURN p")

	# We compute the probabilities of the type of the next sentence for sequences of 5 sentences max
	for length in range(1,5):
		probas = buildProbas(dialogues, length, graph)
		buildTreeStats(probas, graph)
