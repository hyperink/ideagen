import digg_api
import gensim
from os import system
from gensim import corpora, models, similarities
from operator import itemgetter, attrgetter
import utils
from utils.stopwords import STOP_WORDS

#import large document file from books.py
"""
requires: 
  numpy, scipy, gensim

sudo easy_install gensim

HOWTO:
   $ sudo apt-get install python-numpy, python-scipy, python-setuptools
   $ sudo easy_install gensim
"""

def processText(corpus):
    """ returns texts and dictionary given corpus """
    #remove stopwords words # disabled
    punctuations = set('\" : , . & / ; ! ( ) [ ] |')

    sw = STOP_WORDS + ['pic', 'pics','video', 'venturebeat']

    stopwords = set(sw)

    #removes punctuations
    for string in enumerate(corpus):
        corpus[string[0]] = removePunctuations(string[1], punctuations)

    #removed words in set(stopwords)
    texts = [[word for word in document.lower().split() if word not in stopwords]
              for document in corpus]

    #tokenize
    allTokens = sum(texts, [])

    #all words that appear just once
    tokensOnce = set(word for word in set(allTokens) if allTokens.count(word) == 1)

    #removes tokens that appear only once (not able to draw correlations)
    texts = [[word for word in text if word not in tokensOnce]
              for text in texts]
    dictionary = corpora.Dictionary(texts)

    return texts, dictionary

def removePunctuations(string, punctuations):
    for punc in punctuations:
        string = " ".join(string.split(punc))
        string = " ".join(string.split())
    return string

def findTopics(dictionary, texts, topics, lda=False, passes=5):
    """ prints topic table given a dictionary, text corpus and topic count """
    topics = int(topics)
    corpus = [dictionary.doc2bow(text) for text in texts]
    id2word = dictionary
    if not lda:
        result = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=id2word, numTopics=10)
    else:
        passes = int(passes)
        result = gensim.models.ldamodel.LdaModel(corpus=corpus,
                id2word=id2word, numTopics=topics, update_every=0,
                passes=passes)
    return result

def do_digg(lda=True, topicNum=20, passes=1, printOut=True):
    texts, dictionary = processText(digg_api.get_corpus())
    result = findTopics(dictionary=dictionary, 
                        texts=texts, 
                        topics=topicNum,
                        lda=lda,
                        passes=passes)
    if printOut:
        result.printTopics(topicNum)
    return result
