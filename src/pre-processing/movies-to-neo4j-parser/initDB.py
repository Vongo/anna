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
    tree = ET.parse('../../../data/MovieDiC_V2_clean.xml')
    root = tree.getroot()
    for movie in root.findall('movie'):
        title = movie.get('title')
        currentMovie = graph.find_one("Movie", 
                property_key="title", 
                property_value = title)
        if currentMovie is None :
            currentMovie = Node("Movie", title=title)
        for cat in get_movies_genres(movie.get('id'), graph):
            print cat
            movie_is_of_type = Relationship(currentMovie, "IS_OF_TYPE", cat)
            graph.create(movie_is_of_type)


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

