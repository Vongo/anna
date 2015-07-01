#!/usr/bin/python

from answerEngineAPI import AnswerEngineAPI

def getAnswer(userLine, history, category):
    anna = AnswerEngineAPI()
    return anna.getAnnasAnswer(userLine, history, category)

print(getAnswer("","",""))
