# Get Anna's answer
# Good SentenceType + movie category + tokens frequency version
labels = db.findNextSentenceType(5,3).split()
sentence = self.getAnswerWithGoodSentenceTypeAndCategoryAndSemanticRelevancy(5, category, labels)
if sentence is None:
    # Good SentenceType + movie category version
    sentence = self.getAnswerWithGoodSentenceTypeAndCategory(category, labels)
    if sentence is None:
        # Good SentenceType version
        sentence = self.getAnswerWithGoodSentenceType(labels)
        if sentence is None:
            # Random version
            sentence = self.getRandomAnswer()