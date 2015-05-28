# PROJECT PROPOSAL - Anna

## Final aim
We want to create a chat bot based on movies punchlines. The main work will be to analyse the input text (user's sentence) and select the appropriate response given the history of the dialogue and the chosen categorie (see next section).

## Source
Our dataset is called *MovieDiC*. It's a XML file which contains ~700 movies' scripts detailing who is speaking and the context of this talk.

**INSERT EXAMPLE**

## Categories
This is a funny option we want to add : the user will be able to select one category (Action, Drama, Mystery, ...) and will get responses pulled out such movies. The "All" option will also be available meaning that all movies should be considered.
The categorization would be achieved with the help of the OMDb API (see here : http://www.omdbapi.com/).

Should the user not pick a category, we'd like to infere one from the mood of the dialogue history. This will be useful to keep the dialogue consistant.

## User Interface
UI is definitely not the core of this project, so we'll keep it as simple as possible. (readable though)