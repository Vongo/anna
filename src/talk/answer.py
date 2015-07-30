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
        # self.findNextSentenceType(history, 5)
        tokTypesUser = histo.getTokensAndType(userLine)
        db.insert(userLine, tokTypesUser) #timeout
        sentence = self.getRandomAnswer(userLine, category)
        tokTypes = histo.getTokensAndType(sentence)
        db.insert(sentence, tokTypes) #timeout
        return sentence

    def findNextSentenceType(self,history,lenghtHisto):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        types =graph.cypher.execute("MATCH (n:Histo)-[r*0..5]->(sh:SentenceHisto)-[is_of_type]->(st:SentenceType) RETURN st.label AS label")
        # Build SentenceType "path"
        listTypes=[]
        for i in range(len(types)/2):
            listTypes.append(types[2*i+1].label +' ' + types[2*i].label)
        # print listTypes


    def getRandomAnswer(self, userLine, category):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        act = None
        try:
            movie = random.randint(1,1)
            dialogue = random.randint(1,10)
            sen = random.randint(1,1)
            id = str(movie) + "_" + str(dialogue) + "_" + str(sen)
            act = graph.find_one("Sentence", property_key="id", property_value=id)
            print act.properties["full_sentence"]
        except:
            act = "FAIL"
            raise
        return act.properties["full_sentence"]

def getAnswer(userLine, history, category):
    anna = AnswerEngineAPI()
    return anna.getAnnasAnswer(userLine, history, category)
