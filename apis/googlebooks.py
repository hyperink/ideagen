import json
import urllib2
#from utils.stopwords import STOP_WORDS

def get_googlebooks_trends(i=None, api_key=None, api_url=None, getJSON=True):
    """
    Gets books from google books. Full spec TBD
    """
    data = urllib2.urlopen(api_url).read()
    if getJSON:
        data['entries'] = get_googlebooks_trends_entries(data)
    return data

def get_googlebooks_trends_entries(data):
    """
    Helper function which traverses the returned data and turns it
    into a clean list of three-tuples: (entry_id, content, score/metric)
    """
    return data
