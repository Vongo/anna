separators = [".","that",":",";","?","!",",","what","-","..."] # that separate naive propositions
MYSELF_NEAT_IDS = [["My", "name", "is"], ["my", "name", "is"]] # The locutor is definitely speaking about himself.
MYSELF_COMP_IDS = [["I", "am"]] # The locutor can be speaking about his name, but not always ("I am in Berlin", "I am French").

# Splits a sentence (represented as a list of words and symbols) in two parts around a keyword or a keysign.
# Returns the two parts. Note that the key mentioned above disappears from the sentence.
def splitOnKeyword(proposition, keyword):
    #print "splitOnKeyword :", proposition, keyword
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

# In a sentence (represented as a list of words and symbols), replaces the first occurrence of the symbol "de" by the symbol "to".
def replaceWith(proposition, de, vers):
    #print "replaceWith : ", proposition, de, vers
    sentence, after = splitOnKeyword(proposition, de)
    sentence.extend([vers])
    sentence.extend(after)
    return sentence

# Decides how to replace elements of "names" found in "proposition" (represented as a list of words and symbols).
def replaceNameInProposition(names, proposition):
    #print "replaceNameInProposition : ", proposition
    # We check whether there are elements of "names" in the "proposition"
    for t in proposition :
        if t in names :
            foundName = t
            break
    else :
        # If there are no, we return the proposition "as is"
        return proposition
    # Is the locutor speaking about his name ?
    for id in MYSELF_NEAT_IDS :
        index = [(i, i+len(id)) for i in range(len(proposition)) if proposition[i:i+len(id)] == id]
        if len(index) > 0 :
            return replaceWith(proposition, foundName, "ANNA")
    # Is the locutor speaking about himself ?
    for id in MYSELF_COMP_IDS :
        index = [(i, i+len(id)) for i in range(len(proposition)) if proposition[i:i+len(id)] == id]
        if len(index) > 0:
            if len(proposition) >= index[0][1] :
                # Then, are we sure that we are not in the case "I am in Paris" ?
                if proposition[index[0][1]] == foundName:
                    return replaceWith(proposition, foundName, "ANNA")
    # Is the locutor speaking TO someone he'd name ?
    else :
        if 'you' in proposition or len(proposition)==1:
            return replaceWith(proposition, foundName, "USERNAME")
        else :
            # So, he's probably speaking about a third person.
            return replaceWith(proposition, foundName, "EASTER")

# Recursively splits the utterance (represented as a list of words and symbols) into naive atomic sub-propositions,
# and properly replaces elements from "names" in each of these sub-propositions.
def replaceNames(names, utterance):
    #print "replaceNames : ", utterance
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

# Flattens a list of list of list ... into a simple list.
def flatten(*args):
    for x in args:
        if hasattr(x, '__iter__'):
            for y in flatten(*x):
                yield y
        else:
            yield x

# Replaces occurrences of elements of "names" in "utterance" (represented as a list of words and symbols) by semantically appropriate Keywords
def makeSentenceWithNames(names, utterance):
    lowerNames = [x.title() for x in names]
    s_as_list = replaceNames(lowerNames, utterance)
    print s_as_list
    s_as_flat_list = flatten(s_as_list)
    return " ".join(s_as_flat_list)

# Examples for testing the code.
# utterance = "My name is Robert , I am Robert , I am a Robert , and I hate you . Yes , Michel , you heard me : I hate you ! It means that your mother is a man like Jacquie !".split(" ")
# names = "Robert Michel Jacquie".split(" ")
# print makeSentenceWithNames(names, utterance)
