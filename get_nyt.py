#!/usr/bin/env python 

import json
import urllib2
import math
import sys
from time import sleep
import codecs

THINGS = ["mostemailed", "mostshared" ,"mostviewed"]

def get_url(offset, thing="mostemailed"):
    return "http://api.nytimes.com/svc/mostpopular/v2/%s/all-sections/30?offset=%s&api-key=434edd0950e1662f9e41a6cbdb9aa8dd:5:64718441" % (thing, offset)

def get_number(offset, thing="mostemailed"):
    result = get_content(offset, thing)
    return result['num_results']

def get_content(offset, thing="mostemailed"):
    url_in = get_url(offset, thing)
    url = urllib2.urlopen(url_in)
    response = url.read()
    url.close()
    result = json.loads(response)
    return result

def get_all(thing="mostemailed"):
    number = get_number(0, thing)
    results = []
    final = get_content(0)
    for i in range(int(math.ceil(number / 20))):
        offset = i * 20
        print("Pinging: %s" % get_url(offset, thing))
        results += get_content(offset)["results"]
        sleep(1)
    final["results"] = results
    return final

def run(filename, thing="mostemailed", dryrun=False):
    result = get_all(thing)
    js = json.dumps(result)
    if not dryrun:
        try:
            f = open(filename, 'w')
            f.write(js)
            f.close()
        except:
            print(js)

def parse(filename):
    f = codecs.open(filename, 'r', 'utf-8')
    content = f.read()
    f.close()
    data = json.loads(content)
    for article in data["results"]:
        print(article["title"].encode('utf-8'))

def hello(filename):
    print("Hello, %s" % filename)

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'output.json'
    method = sys.argv[2] if len(sys.argv) > 2 else 'run'
    func = globals()[method]
    func(filename)
