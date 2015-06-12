from py2neo import Graph,Node, Relationship, authenticate
from py2neo.server import GraphServer
import json

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

server = GraphServer("../../../neo4j-2.2.0")
server.start()
graph=server.graph
create_constraints(graph.schema)
create_categories_nodes(graph)
server.stop()

