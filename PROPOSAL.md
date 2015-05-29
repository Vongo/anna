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

Should the user not pick a category, we'd like to infere one from the mood of the dialogue history. This will be useful to keep the dialogue consistant.

## Learning
Depending on time, we plan to add a Machine Learning component which might give Anna the ability to learn from her mistakes. An "evaluation" mode would be available for the user, in which he could rank each of Anna's answers. This evaluation would be then used to enhance Anna's ability to choose a proper answer.

## User Interface
UI is definitely not the core of this project, so we'll keep it as simple as possible. (readable though)

## Evaluation
### Modular evaluation
Some components (Category detection, Model structure, …) will be evaluated independently and automatically using objective metrics.

### User evaluation
The user will be given the opportunity to evaluate the whole platform. Thus he will rank the relevancy of each of Anna's answers, in a scale from 0 (irrelevant) to 5 (human answer). 

### Cross-evaluation
Should we implement the ML component, we might evaluate its influence by comparing the results of blind user evaluations on both raw and evolved versions of the platform.
