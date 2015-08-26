from py2neo import Node, Relationship
from py2neo.server import GraphServer
from collections import defaultdict
import time

# Create and store the fist nodes of the statistic tree
def initStatsGraph(graph):
	"""
    Create and store the fist nodes of the statistic tree

    @type  graph: GraphServer
    @param graph: The graph
    """	
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

# Retrieve the type of a sentence
def getType(sentence, graph):
	"""
	Retrieve the type of a sentence

	@type  sentence: Node
	@param sentence: The current sentence node

	@type  graph: GraphServer
	@param graph: The graph

	@return: List of SentenceType
    """	
	typesNodes = graph.cypher.execute("MATCH (s:Sentence{id:'"+sentence.properties['id']+"'})--(t:SentenceType) RETURN t")

	if len(typesNodes) == 3:
		return 'greeting'
	elif typesNodes[1]['t'].properties['label'] == 'negative' or typesNodes[1]['t'].properties['label'] == 'positive':
		return typesNodes[0]['t'].properties['label'] + ' ' + typesNodes[1]['t'].properties['label']
	else:
		return typesNodes[1]['t'].properties['label'] + ' ' + typesNodes[0]['t'].properties['label']

# Compute the probas given the occurences of types of sentence following a sequence of sentence
def computeProbas(occurences):
	"""
    Compute the probas given the occurences of types of sentence following a sequence of sentence

    @type  occurences: dict
    @param occurences: Dictionary of occurences

    @return: Dictionary of probabilities
    """	
	probas = defaultdict(lambda: defaultdict(int))

	for sType, typesDico  in occurences.iteritems():

		total_sentence = 0.0
		for s2Type in typesDico:
			total_sentence = total_sentence + typesDico[s2Type]

		for s2Type in typesDico:
			probas[sType][s2Type] = typesDico[s2Type]/total_sentence

	return probas

# Compute the probabilities of the types of the following sentences for sequences of given length
def buildProbas(dialogues, length, graph):
	"""
	Compute the probabilities of the types of the following sentences for sequences of given length

	@type  dialogues: RecordList
	@param dialogues: All the dialogues

	@type  length: integer
	@param length: Length of the sequences we study

	@type  graph: GraphServer
	@param graph: The graph

	@return: Dictionary of probabilities
    """	
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

# Build query to retrieve TypeSentence node
def buildQuery(strLabels):
	"""
    Build query to retrieve TypeSentence node

    @type  strLabels: string
    @param strLabels: Considered SentenceType's labels

    @return: The string of the query
    """	
	queryString = "MATCH (:Stats)"
	labels = strLabels.split('-')
	for label in labels:
		if label == labels[-1]:
			queryString = queryString + '--(node:TypeStat{label:"'+label.lstrip().rstrip()+'"})'
		else:
			queryString = queryString + '--(:TypeStat{label:"'+label.lstrip().rstrip()+'"})'

	queryString = queryString + ' RETURN node'

	return queryString

# Insert new TypeSentence node in the stats tree
def buildTreeStats(probas, graph):
	"""
    Insert new TypeSentence node in the stats tree

    @type  probas: dict
    @param probas: Dictionary of probabilities

    @type  graph: GraphServer
    @param graph: The graph

    """	
	for key, Dval in probas.iteritems():
		query = buildQuery(key)
		node = graph.cypher.execute(query)

		for v in Dval:
			newNode = Node("TypeStat", label=v, prob=Dval[v])
			has = Relationship(node[0]["node"], 'has', newNode)
			graph.create(has)

# Function called once after the initialisation of the database to build the statistic tree
def buildStats(graph):
	"""
    Function called once after the initialisation of the database to build the statistic tree 

    @type  graph: GraphServer
    @param graph: The graph
    """	
	# retrieve all the dialogues in the db
	dialogues = graph.cypher.execute("MATCH p=(d:Dialogue)-[:IS_COMPOSED_OF]-(s1:Sentence{order:0})-[:sentence_followed_by*]-(s:Sentence) WHERE length(p)=toInt(d.n_utterances) RETURN p")

	# We compute the probabilities of the type of the next sentence for sequences of 5 sentences max
	for length in range(1,5):
		probas = buildProbas(dialogues, length, graph)
		buildTreeStats(probas, graph)
