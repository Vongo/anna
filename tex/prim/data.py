# Open the JSON file containing all details
with open(theJSONFilePath) as data_file:
	allMoviesDetails = json.load(data_file)
	# Parse the movies XML file
	tree = ET.parse(theXMLFilePath)
	root = tree.getroot()
	# Browse the elements tree
	for movie in root.findall('movie'):
		currentDetails = allMoviesDetails[movie.get('id')]
		# Do something now and have fun