# anna

## User interface

## History analysis

## Movies categorization
### What is it ?
This small script extract movies from a clean XML file, get their titles and query it to the OMDB API.
Then we create 3 JSON files in order to store the movies "Genre": 
 - Genre's  name - Genre's id
 - Movies per genre
 - Genres per movie
There are 27 categories (26 + "N/A").

### How to use ?
 1. Make sure that you have a clean XML file (clean means readable, for instance : no '&') located in the */source* folder.
 2. Make sure that you are connected to the Internet. 
 3. Simply run : **python /movies-categorization/scripts/categorization.py**
 4. Enjoy the outputs in the */outputs* folder.
