import digg_api
import semantic_analysis

#KEYWORDS
# bow => Bag Of Words -> [(2,3),(1,3)]
# low => List Of Words -> ['bow', 'wow', 'lol']

# Actual digg titles
title_corp = digg_api.get_corpus() #deterministic

#bow + dictionary of tokens
texts, dictionary = semantic_analysis.processText(title_corp) #texts is deterministic

# corpus [(tokenId, count), (tokenId, count), ...]
corpus = [dictionary.doc2bow(text) for text in texts] # n bag of words'

# lol trained model brah
ldsa = semantic_analysis.do_digg(printOut=False)

# bow -> text bow
bow_low = dict(map(lambda tup: (str(tup[1]), texts[tup[0]]), enumerate(corpus)))

N = 0

# a single string rep of bow
bow = str(corpus[N])

def get_title(low, title_corp=title_corp):
    if not low:
        return []
    def low_in_title(l, title):
        result = all([word.lower() in title.lower() for word in l])
        return result
    return filter(lambda title: low_in_title(low, title), title_corp)

def get_low(bow):
    return bow_low[str(bow)]

def get_max(topic_list):
    return max(topic_list, key=lambda tup: tup[1])

# get dat real title from the nth item in the corpus
#print(title_corp[N])
#print(bow_low[bow])
#print(get_title(bow_low[bow], title_corp))


test_corpus = corpus[:9]
#print(map(lambda bow: get_title(bow_low[str(bow)]), test_corpus))
print(map(lambda entry: (get_max(ldsa[entry]), get_title(get_low(entry))), test_corpus))



