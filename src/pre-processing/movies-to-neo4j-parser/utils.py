from py2neo import Node
import json

def get_cat_label(idCat):
	with open('../movies-categorization/outputs/categories.json') as data_file:    
		data = json.load(data_file)
		for cat, idC in data.items():
			if idC == idCat:
				return cat

def get_movies_genres(movieID, graph):
	with open('../movies-categorization/outputs/categoriesPerMovie.json') as data_file:    
		genresNodes = []
		data = json.load(data_file)
		for idCat in data[movieID]:
			genresNodes.append(
				graph.find_one("Category", 
				property_key="label", 
				property_value = get_cat_label(idCat)))
		return genresNodes 