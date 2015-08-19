#!/usr/bin/python
import nltk;
from py2neo import Graph, Node, Relationship
from py2neo.server import GraphServer
import random, sys
sys.path.insert(0, '../talk')
sys.path.insert(0, '../../talk')
import histo
import db
import names

class AnswerEngineAPI(object):
    """Defines the contract for requesting an answer given a dialogue history and a user's answer."""
    graph = None

    def __init__(self):
        super(AnswerEngineAPI, self).__init__()

    def getAnnasAnswer(self, userLine, category):
        tokTypesUser = histo.getTokensAndType(userLine)
        db.insert(userLine, tokTypesUser) #timeout

        #Get Anna's answer
        # Good SentenceType + movie category version
        sentence = self.getAnswerWithGoodSentenceTypeAndCategory(5,3,category)
        if sentence is None:
            # Good SentenceType version
            sentence = self.getAnswerWithGoodSentenceType(5,3)
            if sentence is None:
                # Random version
                sentence = self.getRandomAnswer()
        chars = db.get_sentencesMovieCharacters(sentence[1]) #[1] = sentence id
        tokTypes = histo.getTokensAndType(sentence[0]) #[0] = full sentence
        sentenceWithNames = names.makeSentenceWithNames(chars+tokTypes[2], nltk.word_tokenize(sentence[0]))
        db.insert(sentenceWithNames, tokTypes) #timeout
        return sentenceWithNames

    def getRandomAnswer(self):
        print "In Random"
        server = GraphServer("../../../neo4j")
        graph = server.graph
        act = None
        try:
            movie = random.randint(1,sum(1 for _ in graph.find("Movie")))
            print movie
            dialogue = random.randint(0,100)
            print dialogue
            sen = random.randint(0,sum(1 for _ in graph.find_one("Dialogue", property_key="id", property_value=str(movie) + "_" + str(dialogue)).match_outgoing(rel_type="IS_COMPOSED_OF")))
            id = str(movie) + "_" + str(dialogue) + "_" + str(sen)
            print id
            act = graph.find_one("Sentence", property_key="id", property_value=id)
            print act.properties["full_sentence"]
        except:
            act = "FAIL"
            raise
        return act.properties["full_sentence"], act.properties["id"]

    def getAnswerWithGoodSentenceType(self, lenghtHisto, depthHisto):
        print "In SentenceType"
        server = GraphServer("../../../neo4j")
        graph = server.graph
        labels = db.findNextSentenceType(lenghtHisto,depthHisto).split()
        print labels
        # MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:'positive'}), (n:Sentence)-[:is_of_type]->(:SentenceType{label:'affirmative'}) RETURN n LIMIT 25
        sentencesQuery = "MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[0]+"\'}), (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[1]+"\'}) RETURN n.full_sentence AS sentence, n.id AS id LIMIT 100"
        records = graph.cypher.execute(sentencesQuery)
        if len(records) == 0:
            return None
        else:
            index = random.randint(0,len(records))
            print records[index]
            return (records[index].sentence,records[index].id)

    def getAnswerWithGoodSentenceTypeAndCategory(self, lenghtHisto, depthHisto, categoryString):
        print "In SentenceType + Category"
        server = GraphServer("../../../neo4j")
        graph = server.graph
        labels = db.findNextSentenceType(lenghtHisto,depthHisto).split()
        print labels
        # MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:'affirmative'}),
        # (n:Sentence)-[:is_of_type]->(:SentenceType{label:'positive'}),
        # (n:Sentence)<-[:IS_COMPOSED_OF]-(:Dialogue)<-[:IS_COMPOSED_OF]-(:Movie)-[:IS_OF_TYPE]->(:Category{label:'Crime'})
        # RETURN n.full_sentence AS sentence
        sentencesQuery = "MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[0]+"\'}), (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[1]+"\'}), (n:Sentence)<-[:IS_COMPOSED_OF]-(:Dialogue)<-[:IS_COMPOSED_OF]-(m:Movie)-[:IS_OF_TYPE]->(:Category{label:\'"+categoryString+"\'}) RETURN m.title AS movie_title,n.full_sentence AS sentence, n.id AS id LIMIT 100"
        records = graph.cypher.execute(sentencesQuery)
        if len(records) == 0: # No sentences matching the query
            return None
        else:
            index = random.randint(0,len(records))
            print records[index]
            return (records[index].sentence,records[index].id)

    def getAnswerWithGoodSentenceTypeAndCategoryAndSemanticRelevancy(self, lenghtHisto):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        distribution = db.computeHistoTokenFrequency(lenghtHisto)
        return None



def getAnswer(userLine, category):
    anna = AnswerEngineAPI()
    return anna.getAnnasAnswer(userLine, category)
