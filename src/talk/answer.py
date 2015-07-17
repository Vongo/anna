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

    def getAnnasAnswer(self, userLine, history, category):
        sentence = self.getRandomAnswer(userLine, category)
        tokTypes = histo.getTokensAndType(sentence)
        db.insert(sentence, tokTypes) #timeout
        return sentence

    def getRandomAnswer(self, userLine, category):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        act = None
        try:
            movie = random.randint(1,700)
            dialogue = random.randint(1,50)
            sen = random.randint(1,3)
            id = str(movie) + "_" + str(dialogue) + "_" + str(sen)
            act = str(graph.find_one("Sentence", property_key="id", property_value=id))
            print act
        except:
            act = "FAIL"
            raise
        return act

def getAnswer(userLine, history, category):
    anna = AnswerEngineAPI()
    return anna.getAnnasAnswer(userLine, history, category)
