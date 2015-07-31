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

        # Random version
        # sentence = self.getRandomAnswer()

        # Good SentenceType version
        sentence = self.getAnswerWithGoodSentenceType(5,3)

        # Good SentenceType + movie category version
        # sentence = self.getAnswerWithGoodSentenceTypeAndCategory(5,3)
        
        tokTypes = histo.getTokensAndType(sentence)
        db.insert(sentence, tokTypes) #timeout
        return sentence

    def getRandomAnswer(self):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        act = None
        try:
            movie = random.randint(0,len(graph.find("Movie")))
            dialogue = random.randint(0,10)
            sen = random.randint(1,1)
            id = str(movie) + "_" + str(dialogue) + "_" + str(sen)
            act = graph.find_one("Sentence", property_key="id", property_value=id)
            print act.properties["full_sentence"]
        except:
            act = "FAIL"
            raise
        return act.properties["full_sentence"]

    def findNextSentenceType(self,lenghtHisto, depthHisto):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        types =graph.cypher.execute("MATCH (n:Histo)-[r*0.."+str(lenghtHisto)+"]->(sh:SentenceHisto)-[is_of_type]->(st:SentenceType) RETURN st.label AS label")
        # Build SentenceType "path"
        listTypes=[]
        for i in range(len(types)/2):
            listTypes.append(types[2*i+1].label +' ' + types[2*i].label)

        # Sublist with the good length
        if len(listTypes) > depthHisto:
            queryTypes = listTypes[-depthHisto:]
        else:
            queryTypes = listTypes
        # Model query :
        queryString= "MATCH (s:Stats)"
        for label in queryTypes:
            queryString+="-->(:TypeStat{label:\'" + label +"\'})"
        queryString+="-->(ts:TypeStat) RETURN ts.label AS label ORDER BY ts.prob DESC LIMIT 1"
        nextType = graph.cypher.execute(queryString)
        return nextType[0].label

    def getAnswerWithGoodSentenceType(self, lenghtHisto, depthHisto):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        labels = self.findNextSentenceType(lenghtHisto,depthHisto).split()
        print labels
        # MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:'positive'}), (n:Sentence)-[:is_of_type]->(:SentenceType{label:'affirmative'}) RETURN n LIMIT 25
        sentencesQuery = "MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[0]+"\'}), (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[1]+"\'}) RETURN n.full_sentence AS sentence LIMIT 100"
        records = graph.cypher.execute(sentencesQuery)
        index = random.randint(0,99)
        print records[index].sentence
        return records[index].sentence

    def getAnswerWithGoodSentenceTypeAndCategory(self, lenghtHisto, depthHisto, categoryString):
        server = GraphServer("../../../neo4j")
        graph = server.graph
        labels = self.findNextSentenceType(lenghtHisto,depthHisto).split()
        print labels
        # MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:'affirmative'}), 
        # (n:Sentence)-[:is_of_type]->(:SentenceType{label:'positive'}),
        # (n:Sentence)<-[:IS_COMPOSED_OF]-(:Dialogue)<-[:IS_COMPOSED_OF]-(:Movie)-[:IS_OF_TYPE]->(:Category{label:'Crime'})
        # RETURN n.full_sentence AS sentence 
        sentencesQuery = "MATCH (n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[0]+"\'}), "+
        "(n:Sentence)-[:is_of_type]->(:SentenceType{label:\'"+labels[1]+"\'}) "+
        "(n:Sentence)<-[:IS_COMPOSED_OF]-(:Dialogue)<-[:IS_COMPOSED_OF]-(:Movie)-[:IS_OF_TYPE]->(:Category{label:\'"+categoryString+"\'}) " +
        "RETURN n.full_sentence AS sentence LIMIT 100"
        records = graph.cypher.execute(sentencesQuery)
        index = random.randint(0,99)
        print records[index].sentence
        return records[index].sentence

def getAnswer(userLine, category):
    anna = AnswerEngineAPI()
    return anna.getAnnasAnswer(userLine, category)
