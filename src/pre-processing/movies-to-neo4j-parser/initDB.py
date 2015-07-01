from py2neo import Graph,Node, Relationship, authenticate
from py2neo.server import GraphServer
from utils import *
import json
import xml.etree.ElementTree as ET

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

def create_categories_nodes(graph):
    with open('../movies-categorization/outputs/categories.json') as data_file:    
        data = json.load(data_file)
        for label in data.keys():
            cat = Node("Category", label=label)
            graph.create(cat)

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

def parseMoviesXML(graph):
    tree = ET.parse('../../../data/1movie.xml')
    root = tree.getroot()
    for movie in root.findall('movie'):
        speakers={}
        # Create movie Node and link it to its categories
        title = movie.get('title')
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
            for i in range(0, int(dialogue.get('n_utterances'))):
                currentSentence = graph.find_one("Sentence", 
                    property_key="id", 
                    property_value = movie.get('id')+"_"+dialogue.get('id')+"_"+str(i))
                if currentSentence is None :
                    currentSentence = Node("Sentence", id=movie.get('id')+"_"+dialogue.get('id')+"_"+str(i), full_sentence=dialogue[3+(4*i)].text)
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


server = GraphServer("../../../neo4j")
server.start()
graph=server.graph
try:
    create_constraints(graph.schema)
    create_categories_nodes(graph)
    create_sentence_types(graph)
    parseMoviesXML(graph)
except:
    raise
finally:
    server.stop()

