separators = [".","that",":",";","?","!",",","what","-"]
MYSELF_NEAT_IDS = [["My", "name", "is"], ["my", "name", "is"]]
MYSELF_COMP_IDS = [["I", "am"]]

def splitOnKeyword(proposition, keyword):
    print "splitOnKeyword :", proposition, keyword
    before = []
    after = []
    weAreBefore = True
    for t in proposition:
        if weAreBefore :
            if t == keyword:
                weAreBefore = False
            else :
                before.append(t)
        else :
            after.append(t)
    return before, after

def replaceWith(proposition, de, vers):
    print "replaceWith : ", proposition, de, vers
    sentence, after = splitOnKeyword(proposition, de)
    sentence.extend([vers])
    sentence.extend(after)
    return sentence

def replaceNameInProposition(names, proposition):
    print "replaceNameInProposition : ", proposition
    for t in proposition :
        if t in names :
            foundName = t
            break
    else :
        return proposition
    for id in MYSELF_NEAT_IDS :
        index = [(i, i+len(id)) for i in range(len(proposition)) if proposition[i:i+len(id)] == id]
        if len(index) > 0 :
            return replaceWith(proposition, foundName, "ANNA")
            break
    else :
        if 'you' in proposition :
            return replaceWith(proposition, foundName, "USERNAME")
        else :
            return replaceWith(proposition, foundName, "EASTER")

def replaceNames(names, utterance):
    print "replaceNames : ", utterance
    pP = utterance
    for t in utterance:
        if t in separators :
            pP, after = splitOnKeyword(utterance, t)
            sep = t
            if len(after) > 1 :
                pS = replaceNames(names, after)
                break
    else :
        return [replaceNameInProposition(names, pP), sep]
    return [replaceNameInProposition(names, pP), sep, replaceNameInProposition(names, pS)]

def flatten(*args):
    for x in args:
        if hasattr(x, '__iter__'):
            for y in flatten(*x):
                yield y
        else:
            yield x

def makeSentenceWithNames(names, utterance):
    lowerNames = [x.title() for x in names]
    s_as_list = replaceNames(lowerNames, utterance)
    print s_as_list
    s_as_flat_list = flatten(s_as_list)
    return " ".join(s_as_flat_list)

# utterance = "My name is Robert , and I fuck you . Yes , Michel , you heard me : I fuck you ! It means that your mother is a slut like Jacquie !".split(" ")
# names = "Robert Michel Jacquie".split(" ")
#... and the wild chase through Times Square ended with the suspect , Oleg Razgul, escaping . The fire department has identified the fire marshal involved in the failed pursuit as Jordy Warsaw .
# ... before Emil boards the police boat and heads for Rykers Island where he will be checked into the psyche ward , I want to say one last word to you all ... As you know , Emil was coerced by Oleg Razgul into committing these murders , yet Oleg is still out in the street , a free man , filming gruesome murders ... My client and I hope he is brought to justice in the near future .
