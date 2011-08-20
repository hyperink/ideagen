from utils.util import prune
from collections import defaultdict
from utils.stopwords import STOP_WORDS
import urllib2
import json

def get_wtt_trends(i=None, api_key=None, api_url=None, getJSON=True):
    """
    Issues a GET call using What The Trend's REST interface and
    returns results in JSON (or text if getJSON set to false)
    """
    data = urllib2.urlopen(api_url).read()
    if getJSON:
        data = json.loads(data)
        data['freq'] = get_wtt_trends_freq(data)
    return data

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
