# PROJECT PROPOSAL - Anna

## Final aim
We want to create a chat bot based on movies punchlines. The main work will be to analyse the input text (user's sentence) and select the appropriate response given the history of the dialogue and the chosen categorie (see next section).

## Source
Our dataset is called *MovieDiC*. It's a XML file which contains ~700 movies' scripts detailing who is speaking and the context of this talk.

**XML structure**
```xml
	<movies>﻿
		<movie id="1" title="12 Monkeys">
			<dialogue id="2" n_utterances="3">
			   <speaker>COLE</speaker>
			      <mode></mode>
			      <context>JOSE's face is almost lost in shadow. </context>
			      <utterance>Ssssst! Jose, what's going on?</utterance>
			   <speaker>JOSE</speaker>
			      <mode></mode>
			      <context>JOSE immediately rolls ...</context>
			      <utterance>"Volunteers" again.</utterance>
			   <speaker>SCARFACE</speaker>
			      <mode></mode>
			      <context>The PRISONERS in the other cages...</context>
			      <utterance>"Volunteer duty".</utterance>
			</dialogue>
		</movie>
	</movies>
```
## Categories
This is a funny option we want to add : the user will be able to select one category (Action, Drama, Mystery, ...) and will get responses pulled out such movies. The "All" option will also be available meaning that all movies should be considered.
The categorization would be achieved with the help of the OMDb API (see here : http://www.omdbapi.com/).

## User Interface
UI is definitely not this project's core so we'll keep it as simple as possible. (readable tho)