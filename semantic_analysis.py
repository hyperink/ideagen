import digg_api
import gensim
from os import system
from gensim import corpora, models, similarities
from operator import itemgetter, attrgetter

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
    punctuations = set('')

    #punctuations = set('\" : - , . & / ; ! ( )')

    stopwords = set('for a of the and to in with'.split())

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

def findTopics(dictionary, texts, topics, lda=False, passes=20):
    """ prints topic table given a dictionary, text corpus and topic count """
    topics = float(topics)
    corpus = [dictionary.doc2bow(text) for text in texts]
    id2word = dictionary
    if not lda:
        result = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=id2word, num_topics=topics)
    else:
        passes = int(passes)
        result = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=topics, update_every=0, passes=passes)
    return result


"""
Example data structures
  corpus: ['content', 'content2', 'content3', ...]
  entry: (key, content, metric)
  classified entry: (key, content, metric, topic)
"""

def train(corpus, lda=False, topicNum=20, passes=5, printOut=False):
    """
    corpus -> trained model
    usage:
      >>> trained_model = do_training(['cat came home', 'dog went home', ...])
    """
    texts, dictionary = processText(corpus)
    result = findTopics(dictionary=dictionary, 
                        texts=texts, 
                        topics=topicNum, 
                        lda=lda)
    if printOut:
        result.print_topics(topicNum)
    return result

def findtopic(content, model):
  """
  Classifies a piece of content into a most likely topic
  (content, model) -> topic_id

  usage:
    >>> topic_id = findtopic("This is an example new title", model)
  """
  def getmax(topic_list):
    return 1
  topics = model[bow(content)] # a list of topic probabilities
  return getmax(topics) # most probable topic

def classify(entries, model):
  """
  Takes entries (3 tuple) + model 
  (entries, model) -> (classified_entries) (4 tuple)

  usage:
    >>> classified_entries = classify(entries, train(corpus))
  """
  map(entries, lambda entry: (entry[0], entry[1], entry[2], findtopic(entry[1], model)))
  pass

