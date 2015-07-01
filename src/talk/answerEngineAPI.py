#!/usr/bin/python
from py2neo import Graph
from py2neo.server import GraphServer

import os

class AnswerEngineAPI(object):
    """Defines the contract for requesting an answer given a dialogue history and a user's answer."""
    graph = None

    def __init__(self):
        super(AnswerEngineAPI, self).__init__()
        
    def getAnnasAnswer(self, userLine, history, category):
        return self.getRandomAnswer(userLine, category)

    def getRandomAnswer(self, userLine, category):
        server = GraphServer("../../neo4j")
        server.start()
        graph = server.graph
        try:
            print self.graph.size
            self.graph.open_browser()
        except:
            raise
        finally:
            server.stop()

        act = None
        if act == None :
            return "FAiL"
        else :
            return "Ta maman elle est pubayre ?"
