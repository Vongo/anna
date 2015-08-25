from py2neo import Graph,Node, Relationship, authenticate
from py2neo.server import GraphServer
from utils import *
import json
import xml.etree.ElementTree as ET
import sys
sys.path.insert(0, '../../talk')
import histo
sys.path.insert(0, '../')
import buildStats
from py2neo.packages.httpstream import http

# DB constraints
def create_constraints(schema):
    # Movies
    schema.create_uniqueness_constraint("Movie","title")
    # Categories
    schema.create_uniqueness_constraint("Category","label")
    # Sentences type
    schema.create_uniqueness_constraint("SentenceType","label")
    # Tokens
    schema.create_uniqueness_constraint("Token","label")
    # Dialogues
    schema.create_uniqueness_constraint("Dialogue","id") # id = idMovie_idDialogue
    # Dialogues
    schema.create_uniqueness_constraint("Sentence","id") # id = idMovie_idDialogue_idSentence
    # Characters
    schema.create_index("Character","full_name")

# Create all categories nodes
def create_categories_nodes(graph):
    with open('../movies-categorization/outputs/categories.json') as data_file:
        data = json.load(data_file)
        for label in data.keys():
            cat = Node("Category", label=label)
            graph.create(cat)

# Create sentence types nodes
def create_sentence_types(graph):
    # Interrogative
    inter = Node("SentenceType", label="interrogative")
    graph.create(inter)
    # Exclamation
    excl = Node("SentenceType", label="exclamation")
    graph.create(excl)
    # Affirmative
    aff = Node("SentenceType", label="affirmative")
    graph.create(aff)
    # Negative
    neg = Node("SentenceType", label="negative")
    graph.create(neg)
    # Positive
    pos = Node("SentenceType", label="positive")
    graph.create(pos)
    # Greeting
    greet = Node("SentenceType", label="greeting")
    graph.create(greet)

# Main function, parse the whole XML file into our graph model
def parseMoviesXML(graph):
    tree = ET.parse('../../../data/1movie.xml')
    root = tree.getroot()
    for movie in root.findall('movie'):
        speakers={}
        # Create movie Node and link it to its categories
        title = movie.get('title')
        print "  Parsing movie : " + title + " ..."
        currentMovie = graph.find_one("Movie",
                property_key="title",
                property_value = title)
        if currentMovie is None :
            currentMovie = Node("Movie", title=title)
        for cat in get_movies_genres(movie.get('id'), graph):
            movie_is_of_type = Relationship(currentMovie, "IS_OF_TYPE", cat)
            graph.create_unique(movie_is_of_type)

        # Create dialogues
        for dialogue in movie.findall('dialogue'):
            currentDial = graph.find_one("Dialogue",
                    property_key="id",
                    property_value = movie.get('id')+"_"+dialogue.get('id'))
            if currentDial is None :
                currentDial = Node("Dialogue", id=movie.get('id')+"_"+dialogue.get('id'), n_utterances=dialogue.get('n_utterances'))
            movie_is_composed_of = Relationship(currentMovie,"IS_COMPOSED_OF", currentDial)
            graph.create_unique(movie_is_composed_of)
            # Sentences
            last_sentence = None;
            for i in range(0, int(dialogue.get('n_utterances'))):
                currentSentence = graph.find_one("Sentence",
                    property_key="id",
                    property_value = movie.get('id')+"_"+dialogue.get('id')+"_"+str(i))
                if currentSentence is None :
                    currentSentence = Node("Sentence", id=movie.get('id')+"_"+dialogue.get('id')+"_"+str(i), full_sentence=dialogue[3+(4*i)].text, order=i)
                dial_is_composed_of = Relationship(currentDial,"IS_COMPOSED_OF", currentSentence)
                graph.create_unique(dial_is_composed_of)
                # Speaker
                if dialogue[4*i].text in speakers:
                    currentSpeaker = speakers[dialogue[4*i].text]
                else:
                    potSpeakers = graph.find("Character",
                        property_key="full_name",
                        property_value = dialogue[4*i].text)
                    currentSpeaker = None
                    for speaker in potSpeakers:
                        if graph.match_one(start_node=currentMovie, end_node=speaker) is not None:
                            currentSpeaker = speaker
                    if currentSpeaker is None:
                        currentSpeaker = Node("Character", full_name=dialogue[4*i].text)
                    speakers[dialogue[4*i].text] = currentSpeaker
                sentence_is_spoken_by = Relationship(currentSentence,"IS_SPOKEN_BY", currentSpeaker)
                graph.create_unique(sentence_is_spoken_by)

                #create tokens and sentence type
                tokensAndType = histo.getTokensAndType(currentSentence.properties["full_sentence"])

                for t in xrange(0, len(tokensAndType[1])):
                    sentenceType = graph.find_one("SentenceType", property_key='label', property_value=tokensAndType[1][t])
                    is_of_type = Relationship(currentSentence, "is_of_type", sentenceType)
                    graph.create_unique(is_of_type)

                for token in tokensAndType[0]:
                    token = Node("Token", token=token[0], tag=token[1])
                    is_composed_of = Relationship(currentSentence, "is_composed_of", token)
                    graph.create_unique(is_composed_of)

                if last_sentence != None:
                    sentence_followed_by = Relationship(last_sentence, "sentence_followed_by", currentSentence)
                    graph.create(sentence_followed_by)
                last_sentence = currentSentence

        print "  Done."

# Init historic
def init_histo(graph):
	histo = Node("Histo", label="histo")
	graph.create(histo)

server = GraphServer("../../../neo4j")
server.stop()
print "Starting Neo4j server..."
server.start()
print "Done."
graph=server.graph
try:
    print "Creating constraints..."
    create_constraints(graph.schema)
    print "Done."
    print "Creating categories nodes..."
    create_categories_nodes(graph)
    print "Done."
    print "Creating sentences types..."
    create_sentence_types(graph)
    print "Done."
    print "Parsing Movies XML..."
    parseMoviesXML(graph)
    print "Done."
    print "Initing histo..."
    init_histo(graph)
    print "Done."
    print "Initing Stats..."
    buildStats.initStatsGraph(graph)
    print "Building Stats..."
    buildStats.buildStats(graph)
    print "Stats Done."
except:
    raise
finally:
    server.stop()
    print "Job all done. See you later."