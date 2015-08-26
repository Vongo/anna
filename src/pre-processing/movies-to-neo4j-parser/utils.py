from py2neo import Node
import json

def get_cat_label(idCat):
	"""
	Get the label of a genre given its id

	@type  idCat: integer
	@param idCat: The id of the genre

	@return: The label of the genre
	"""
	with open('../movies-categorization/outputs/categories.json') as data_file:
		data = json.load(data_file)
		for cat, idC in data.items():
			if idC == idCat:
				return cat

# Get genres' nodes for a given movie
def get_movies_genres(movieID, graph):
	"""
    Get the label of a genre given its id

    @type  movieID: integer
    @param movieID: The id of the movie

    @type  graph: GraphServer
    @param graph: The graph

    @return: List of genres' nodes
    """	
	with open('../movies-categorization/outputs/categoriesPerMovie.json') as data_file:    
		genresNodes = []
		data = json.load(data_file)
		for idCat in data[movieID]:
			genresNodes.append(
				graph.find_one("Category", 
				property_key="label", 
				property_value = get_cat_label(idCat)))
		return genresNodes 