import json
import urllib2
#from utils.stopwords import STOP_WORDS

def get_nytimes_trends(i=None, api_key=None, api_url=None, getJSON=True, whichAPI="bestseller"):
    """
    Gets books from google books. Full spec TBD
    """
    try:
        whichAPI = i['whichny']
    except:
        pass
    api_url = api_url[whichAPI] + api_key[whichAPI]
    data = json.loads(urllib2.urlopen(api_url).read())
    if getJSON:
        data['title'] = whichAPI
        data['entries'] = get_nytimes_trends_entries(data)
    return data

def get_nytimes_trends_entries(data):
    """
    Helper function which traverses the returned data and turns it
    into a clean list of three-tuples: (entry_id, content, score/metric)
    """
    return data
