from utils.util import prune
from collections import defaultdict
from utils.stopwords import STOP_WORDS
import urllib2
import json

def get_wtt_trends(i=None, api_key=None, api_url=None, getJSON=True, entries=True, freq=True):
    """
    Issues a GET call using What The Trend's REST interface and
    returns results in JSON (or text if getJSON set to false)
    """
    data = urllib2.urlopen(api_url).read()
    if getJSON:
        data = json.loads(data)
        # Note, these below calls are both linear sweeps 
        # and can be combined together.
        # They were not combined to preserve modularlity
        data['freq'] = get_wtt_trends_freq(data)
        data['entries'] = get_wtt_trends_entries(data)
    return data

def get_wtt_trends_entries(data):
    """
    Returns a list of three-tuples, each containing the
    id of the trend content, the content itself,
    and a heuristic metric -- a score (# tweets)

    usage:
      >>> get_wtt_trends_entries(data) 
      [(trend_id, content, score), ...]
    """
    entries = []
    trends = data['trends']
    for trend in trends:
        trend_id = trend.get('trend_id', None)
        desc = trend.get('description', None)
        query = trend.get('query', None)
        try:
            score = desc['score']
            content = desc['text']
            entries.append((trend_id, content, score))
        except:
            pass
    return entries

def get_wtt_trends_freq(data):
    """
    Takes the results of the What The Trends API, prunes each
    trend description for important words, and returns frequency
    information to determine the most important keywords and
    topics.
    """
    trends = data['trends']
    tags = []
    for trend in trends:
        words = ""
        trend_id = trend.get('trend_id', None)
        desc = trend.get('description', None)
        name = trend.get('name', None)
        query = trend.get('query', None)
        try:
            words += desc['text']
        except:
            pass
        try:
            words += " " + name
        except:
            pass
        try:
            words += " " + query
        except:
            pass
        tags = tags + prune(words.split(), STOP_WORDS)
    if tags:
        d = defaultdict(int)
        for tag in tags:
                d[tag] += 1
        return d
    return tags
