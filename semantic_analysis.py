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

DEFAULT_PASSES = 1
DEFAULT_TOPICS = 10
DEFAULT_LDA = True

def processText(corpus):
    """ returns texts and dictionary given corpus 
    corpus -> (texts, dictionary)

    usage:
      >>> processText(['This is an example title', ...], STOP_WORDS=STOP_WORDS)
    """
    #  note using global variable!!! STOP_WORDS

    #remove stopwords words # disabled
    punctuations = set('\" : , . & / ; ! ( ) [ ] |')

    sw = STOP_WORDS + ['pic', 'pics','video', 'venturebeat']

    stopwords = set(sw)

    #removes punctuations
    for string in enumerate(corpus):
        corpus[string[0]] = removePunctuations(string[1])

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

def removePunctuations(string):
    punctuations = set('\" : , . & / ; ! ( ) [ ] |')
    for punc in punctuations:
        string = " ".join(string.split(punc))
        string = " ".join(string.split())
    return string

def train_model(dictionary, texts, topics=DEFAULT_TOPICS, lda=DEFAULT_LDA, passes=DEFAULT_PASSES):
    """
    (dictionary, texts, topics) -> model
    usage:
        >>> model = train_model(dictionary=dictionary, 
        >>>                     texts=texts, 
        >>>                     topics=topicNum,
        >>>                     lda=lda,
        >>>                     passes=passes)
    """
    topics = int(topics)
    corpus = [dictionary.doc2bow(text) for text in texts]
    id2word = dictionary
    if not lda:
        model = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=id2word, numTopics=10)
    else:
        passes = int(passes)
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                id2word=id2word, numTopics=topics, update_every=0,
                passes=passes)
    return model

"""
Example data structures
  corpus: ['content', 'content2', 'content3', ...]
  entry: (key, content, metric)
  classified entry: (key, content, metric, topic)
"""

def discover(entries, granularity=DEFAULT_TOPICS, lda=DEFAULT_LDA, passes=DEFAULT_PASSES):
  """
  disover ranked topic list
  entries - > ranked topic list

  sub process:

  entries -> corpus -> model, texts, dictionary -> classified entries -> topic metrics -> ranked list

  usage:
    >>> ranked_topic_list = discover(entries)
  """
  model, texts, dictionary = train(corpify(entries), 
                                   topicNum=granularity,
                                   lda=lda,
                                   passes=passes)
  classified_entries = map(classifier(model, dictionary, texts), entries) # [(key, content, metric, class), ...]
  topic_metrics = sum_topics(classified_entries) # [(topic_id, sum_metric), ...]
  named_topics = name_topics(topic_metrics, model, granularity)
  return sorted(named_topics, key=lambda topic: topic[1], reverse=True) # sort by sum_metric

def name_topics(topic_list, model, granularity=20):
  """
  (topicid, metric) -> (topicstring, metric)

  usage:
    >>> name_topics(topic_list)
  """
  topic_dict = model.printTopics(granularity)
  topic_dict[-1] = "No Topic"
  return map(lambda topic: (topic_dict[topic[0]], topic[1]), topic_list)

def docify(content):
  """
  'content title stuff without any of those stopwords like the' -> ['content', 'title', 'stopwords']
  """
  return removePunctuations(content).split()

def corpify(entries):
  """
  [(key, content, metric), ...] -> [content, content, ...]
  
  usage:
    >>> corpus = corpify(entries)
  """
  return map(lambda entry: entry[1], entries)

def train(corpus, lda=DEFAULT_LDA, topicNum=DEFAULT_TOPICS, passes=DEFAULT_PASSES, printOut=False):
    """
    corpus -> (trained model, texts, dictionary)
    usage:
      >>> trained_model, texts, dictionary = train(['the cat came home', 'the dog went home', ...])
    """
    texts, dictionary = processText(corpus)
    return (train_model(dictionary=dictionary, 
                        texts=texts, 
                        topics=topicNum,
                        lda=lda,
                        passes=passes), texts, dictionary)

def bow(content, dictionary):
  """
  content, dictionary -> bow
  """
  return dictionary.doc2bow(docify(content))

def tfidf(content, dictionary, texts):

  """
  content, dictionary, texts -> tfidf vector
  """
  vectorCorpus = [dictionary.doc2bow(text) for text in texts]
  if 'TFIDF' not in globals():
    globals()['TFIDF'] = models.TfidfModel(vectorCorpus)
  tfidfModel = TFIDF
  return tfidfModel[bow(content, dictionary)] # a list of (topic_id, topic_probability)

def findtopic(content, model, dictionary, texts):
  """
  Classifies a piece of content into a most likely topic
  (content, model, dictionary, texts) -> topic_id

  usage:
    >>> topic_id = findtopic("This is an example new title", model, dictionary)
  """
  isLSI = getattr(model, 'addDocuments', False)
  if isLSI:
    topics = model[tfidf(content, dictionary, texts)]
  else:
    topics = model[bow(content, dictionary)] # a list of (topic_id, topic_probability)
  if topics:
    return max(topics, key=lambda tup: tup[1])[0] # most probable topic id
  else:
    return 0

def classifier(model, dictionary, texts):
  """
  (model, dictionary, texts) -> fn(entry): custom_classifier
  """
  return lambda entry: classify(entry, model, dictionary, texts)

def classify(entry, model, dictionary, texts):
  """
  Takes entries (3 tuple) + model 
  (entries, model, dictionary, texts) -> (classified_entries) (4 tuple)

  usage:
    >>> classified_entry = classify(entry, train(corpus)[0])
  """
  return (entry[0], entry[1], entry[2], findtopic(entry[1], model, dictionary, texts))

def sum_topics(classified_entries):
  """
  [(key, content, metric, topicid), ...] -> [(topicid, sum_metric), ...]
  usage:
    >>> topic_list = sum_topics(map(classifier(model, dictionary), entries))
  """
  results = {}
  results[-1] = 0
  for entry in classified_entries:
    key = entry[3]
    if key in results:
      results[key] += entry[2]
    else:
      results[key] = entry[2]
  return results.items()


def print_results(result):
  r = ''
  for topic in enumerate(result):
    r += "#%s: %s (%s)\n" % (topic[0] + 1, topic[1][0], topic[1][1])
  return r
