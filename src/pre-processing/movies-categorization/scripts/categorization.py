from collections import defaultdict
import xml.etree.ElementTree as ET
import urllib, requests, json

def query_movie_api(movieTitle):
    """
    Query OMDb's API by movie's title

    @type  movieTitle: string
    @param movieTitle: The title of the movie.

    @return:  a json object containing OMDb's response
    """

    data = {}
    data['t'] = movieTitle
    data['r'] = 'json'
    url_values = urllib.urlencode(data)
    url = 'http://www.omdbapi.com/'
    full_url = url + '?' + url_values
    r = requests.get(full_url)
    return r.json()

# Modify the title (some of the movie's title in the Dataset are funny)
def generate_clean_title(title):
    """
    Modify the title if needed. Usefull for some cases

    @type  title: string
    @param title: The initial title of the movie.

    @return:  a modified title, most likely to be recognized by OMDb's API
    """

    clean=title
    if title.endswith("The"):
        clean ="The "+title[:-3]
    if title.endswith("A"):
        clean = "A "+title[:-1]
    if title.endswith("An"):
        clean = "An "+title[:-2]
    if " s " in title:
        clean = clean.replace(" s ", "'s ")
    if " ve " in title:
        clean = clean.replace(" ve ", "'ve ")
    if " vs " in title:
        clean = clean.replace(" vs ", " vs. ")
    if " t " in title:
        clean = clean.replace(" t ", "'t ")
    if " ll " in title:
        clean = clean.replace(" ll ", "'ll ")
    return clean

def generate_genre_set(srcFile):
    """
    Generate a set with all possible movies' genres

    @type  srcFile: string
    @param srcFile: Path to the source data file

    @return:  the set of genres.
    """

    genres=set()
    tree = ET.parse(srcFile)
    root = tree.getroot()
    for movie in root.findall('movie'):
        title = movie.get('title')
        title = generate_clean_title(title)
        json = query_movie_api(title)
        if json['Response'] == "True":
            for genre in json['Genre'].split(', '):
                genres.add(genre)
        else:
            print title + " not found"
    return genres

# Export JSON data
def create_and_print_json(genres_set):
    """
    Exports the genres' set to a JSON file

    @type  genres_set: set
    @param genres_set: genres' set
    """

    all_genres=dict.fromkeys(sorted(genres_set))
    id_genre=0
    for genre in genres_set:
        all_genres[genre]=id_genre
        id_genre +=1
        with open('../outputs/categories.json', 'w') as outfile:
            json.dump(all_genres, outfile)

def create_categories_dict():
    """
    Main function to generate Categories' JSON file
    """

    genres = generate_genre_set(srcFile)
    create_and_print_json(genres)

def categorize_movies(srcFile):
    """
    Categorize movies using OMDb's API and exports JSON files

    @type  srcFile: string
    @param srcFile: Path to the source data file
    """

    with open("../outputs/categories.json") as data_file:
        genres = json.load(data_file)

    tree = ET.parse(srcFile)
    root = tree.getroot()
    allMovies=dict()
    allCategories=defaultdict(list)
    

    for movie in root.findall('movie'):
        # print allCategories
        id_movie = movie.get('id')
        title = movie.get('title')
        title = generate_clean_title(title)
        jsonResponse = query_movie_api(title)
        id_genres = []
        if jsonResponse['Response'] == "True": # If movie is find in OMDb
            for genre in jsonResponse['Genre'].split(', '):
                current_id_genre = genres[genre]
                id_genres.append(current_id_genre)
                allCategories[current_id_genre].append(id_movie)
        else:
            id_genres.append(genres['N/A'])
            allCategories[genres['N/A']].append(id_movie)

        allMovies[id_movie]=id_genres
        # Print JSON files
        with open('../outputs/categoriesPerMovie.json', 'w') as outfile:
            json.dump(allMovies, outfile)
        with open('../outputs/moviesPerCategory.json', 'w') as outfile:
            json.dump(allCategories, outfile)

def generate_all_infos_json(srcFile):
    """
    Generate a full JSON file containing all movies' data

    @type  srcFile: string
    @param srcFile: Path to the source data file
    """
    
    print "Extracting movies' details from the OMDB API"
    with open("../outputs/categories.json") as data_file:
        genres = json.load(data_file)

    tree = ET.parse(srcFile)
    root = tree.getroot()
    allInfos = dict()
    for movie in root.findall('movie'):
        id_movie = movie.get('id')
        title = movie.get('title')
        title = generate_clean_title(title)
        print "Processing " + title
        jsonResponse = query_movie_api(title)
        if jsonResponse['Response'] == "True": # Delete useless data
            del jsonResponse['Response']
            del jsonResponse['Rated']
            del jsonResponse['Released']
            del jsonResponse['Writer']
            del jsonResponse['Plot']
            del jsonResponse['Language']
            del jsonResponse['Awards']
            del jsonResponse['Poster']
            del jsonResponse['Metascore']
            del jsonResponse['imdbID']
            del jsonResponse['Type']
            allInfos[id_movie] = jsonResponse
    with open('../outputs/allMovies.json', 'w') as outfile:
            json.dump(allInfos, outfile)

# srcFile = "../../../../data/1movie.xml"
# srcFile = "../../../../data/3movies.xml"
srcFile = "../../../../data/MovieDiC_V2_clean.xml"
# create_categories_dict(srcFile)
# categorize_movies(srcFile)
generate_all_infos_json(srcFile)
