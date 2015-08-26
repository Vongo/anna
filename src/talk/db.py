from py2neo.server import GraphServer
from py2neo import Node,Relationship

HISTO_LENGTH = 5

# Take a sentence and it's associate tokens and type and 
# store all of it in the db as the last sentence of the dialogue
def insert(sentence, tokensAndType):
    """
    Take a sentence and it's associate tokens and type and store all of it in the db as the last sentence of the dialogue

    @type  sentence: string
    @param sentence: The inserted sentence

    @type  tokensAndType: list
    @param tokensAndType: The sentence's tokens and its SentenceTypes
    """		
	server = GraphServer("../../../neo4j")
	graph=server.graph

	# Retrieve all the sentences of the dialogue 
	sentences = graph.cypher.execute("MATCH (n:Histo)-[r*0..5]->(st:SentenceHisto) RETURN st")
	print sentences
	numberOfSentences = len(sentences)

	# Create a node to insert as the last sentence of the dialogue
	sentence = Node("SentenceHisto", sentence=sentence)
	sentenceType = graph.find_one("SentenceType",
                    property_key="label",
                    property_value = tokensAndType[1][0])
	sentenceForm = graph.find_one("SentenceType",
                    property_key="label",
                    property_value = tokensAndType[1][1])
	# Link the sentence with it's type and it's form
	is_of_type = Relationship(sentence, "is_of_type", sentenceType)
	is_of_form = Relationship(sentence, "is_of_type", sentenceForm) # pos / neg
	graph.create(is_of_type)
	graph.create(is_of_form)
	print 'nb sentences : ' + str(numberOfSentences)

	# If we have just started the dialogue we create the root node and store the sentence as its child
	if numberOfSentences == 0:
		histo = graph.find_one("Histo",
								property_key="label",
								property_value = "histo")
		has = Relationship(histo, "is_followed_by", sentence)
		graph.create(has)
	# We only keep an history of the dialogue of HISTO_LENGTH sentences long
	# So we delete the first sentence if the length is of HISTO_LENGTH
	elif numberOfSentences == HISTO_LENGTH:
		graph.cypher.execute("MATCH (n:Histo)-[r:is_followed_by*1]->(:SentenceHisto) FOREACH( rel IN r| DELETE rel)")

		histo = graph.find_one("Histo",
								property_key="label",
								property_value = "histo")
		has = Relationship(histo, "is_followed_by", sentences[1][0])
		graph.create(has)

		is_followed_by = Relationship(sentences[-1][0], "is_followed_by", sentence)
		graph.create(is_followed_by)
	# We insert the sentence in the histo
	else:
		is_followed_by = Relationship(sentences[-1][0], "is_followed_by", sentence)
		graph.create(is_followed_by)

	for token in tokensAndType[0]:
		print token
		tokenNode = graph.find_one("TokenHisto",
							   property_key="token",
							   property_value = token[0])
		if tokenNode is None:
			tokenNode = Node("TokenHisto", token=token[0], pos=token[1])

		is_composed_of = Relationship(sentence, "is_composed_of", tokenNode)
		graph.create(is_composed_of)

# Delete the potential existing historic of dialogue before starting a new one
def clean_histo():
    """
    Delete the potential existing historic of dialogue before starting a new one
    """	
	server = GraphServer("../../../neo4j")
	graph=server.graph
	graph.cypher.execute("MATCH (n:SentenceHisto)-[rels]-(),(t:TokenHisto) delete rels, n,t")

# Extract all the characters from a movie given a sentence of this movie
def get_sentencesMovieCharacters(sentenceId):
    """
    Extract all the characters from a movie given a sentence of this movie

    @type  sentenceId: integer
    @param sentenceId: The id of the sentence

    @return: A RecordList of Characters
    """	
	server = GraphServer("../../../neo4j")
	graph=server.graph
	query = "MATCH (n:Sentence{id:{sentenceId}})<-[r:IS_COMPOSED_OF*2]-(m:Movie), (m:Movie)-[:IS_COMPOSED_OF*2]->(:Sentence)-[IS_SPOKEN_BY]->(c:Character) RETURN COLLECT(DISTINCT c.full_name) as chars"
	results = graph.cypher.execute_one(query, sentenceId=sentenceId)
	return results

# Given a historic length (how far should we look into it), we compute the next sentence type (affirmative positive for instance) using pre-processed statistics
def findNextSentenceType(lenghtHisto, depthHisto):
	"""
	Given a historic length (how far should we look into it), we compute the next sentence type (affirmative positive for instance) using pre-processed statistics

	@type  lenghtHisto: integer
	@param lenghtHisto: The maximal size of the historic

	@type  depthHisto: integer
	@param depthHisto: The number of sentences we consider

	@return: The next sentence's type
	"""	
	server = GraphServer("../../../neo4j")
	graph = server.graph
	types =graph.cypher.execute("MATCH (n:Histo)-[r*0.."+str(lenghtHisto)+"]->(sh:SentenceHisto)-[is_of_type]->(st:SentenceType) RETURN st.label AS label")
	# Build SentenceType "path"
	listTypes=[]
	for i in range(len(types)/2):
	    listTypes.append(types[2*i+1].label +' ' + types[2*i].label)

	# Sublist with the good length
	if len(listTypes) > depthHisto:
	    queryTypes = listTypes[-depthHisto:]
	else:
	    queryTypes = listTypes
	# Model query :
	queryString= "MATCH (s:Stats)"
	for label in queryTypes:
	    queryString+="-->(:TypeStat{label:\'" + label +"\'})"
	queryString+="-->(ts:TypeStat) RETURN ts.label AS label ORDER BY ts.prob DESC LIMIT 1"
	nextType = graph.cypher.execute(queryString)
	return nextType[0].label

# Get the token distribution in the historic, only NN* are taken into account
def computeHistoTokenFrequency(lenghtHisto):
	"""
    Get the token distribution in the historic, only NN* are taken into account

    @type  lenghtHisto: integer
    @param lenghtHisto: The maximal size of the historic

    @return: A RecordList of tokens distribution
    """	
	server = GraphServer("../../../neo4j")
	graph = server.graph
	query = "MATCH (n:Histo)-[:is_followed_by*0.."+str(lenghtHisto)+"]->(sh:SentenceHisto)-[:is_composed_of]->(t:TokenHisto) WHERE t.pos =~ 'NN*' RETURN t.token as token,count(t) as total ORDER by total desc LIMIT 10"
	return  graph.cypher.execute(query)
