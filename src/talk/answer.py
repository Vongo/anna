#!/usr/bin/python

from py2neo import Graph, Node, Relationship
from py2neo.server import GraphServer
import random, sys
sys.path.insert(0, '../talk')
sys.path.insert(0, '../../talk')
import histo
import db

class AnswerEngineAPI(object):
    """Defines the contract for requesting an answer given a dialogue history and a user's answer."""
    graph = None

    def __init__(self):
        super(AnswerEngineAPI, self).__init__()

    def getAnnasAnswer(self, userLine, category):
        tokTypesUser = histo.getTokensAndType(userLine)
        db.insert(userLine, tokTypesUser) #timeout
        sentence = self.getRandomAnswer(userLine, category)
        tokTypes = histo.getTokensAndType(sentence)
        db.insert(sentence, tokTypes) #timeout
        return sentence

    def findNextSentenceType(self,history,lenghtHisto):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        # graph.cypher.execute("MATCH (n:SentenceHisto)-[r]-() WHERE n.sentence=\""+sentences[0]["sentence"]+"\" DELETE n, r")


    def getRandomAnswer(self, userLine, category):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        act = None
        try:
            print "Python " + category
            movie = random.randint(1,1)
            dialogue = random.randint(1,10)
            sen = random.randint(1,3)
            id = str(movie) + "_" + str(dialogue) + "_" + str(sen)
            act = graph.find_one("Sentence", property_key="id", property_value=id)
            print act.properties["full_sentence"]
        except:
            act = "FAIL"
            raise
        return act.properties["full_sentence"]

def getAnswer(userLine, category):
    anna = AnswerEngineAPI()
    return anna.getAnnasAnswer(userLine, category)
