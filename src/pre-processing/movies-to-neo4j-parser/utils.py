from py2neo import Node
import json

# Get the label of a genre given its id
def get_cat_label(idCat):
	with open('../movies-categorization/outputs/categories.json') as data_file:    
		data = json.load(data_file)
		for cat, idC in data.items():
			if idC == idCat:
				return cat

# Get genres' nodes for a given movie
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