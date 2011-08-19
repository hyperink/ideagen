import json
import urllib2

def trendspotter(l=33):
    """
    Goal:
        [stories] -> [('title', diggs)] -> [('topic', diggs)]
    """
    pass

def get_top(l=999):
    """
    Performs HTTP GET over top news stories from digg, returns dictionary of results

    """
    qurl = 'http://services.digg.com/2.0/story.getTopNews?limit=%s' % int(l)
    response = urllib2.urlopen(qurl).read()
    return json.loads(response)

def histogram(diggDict):
    results = {}
    # map [{story}] -> [('topic_clean', 'diggs')]
    tList = map(lambda story: (story['topic']['name'], story['diggs']), diggDict['stories'])
    for tup in tList:
        if tup[0] in results.keys():
            results[tup[0]] += tup[1]
        else:
            results[tup[0]] = tup[1]
    return results

def test(l=3):
    return histogram(get_top(l=l))

"""
Example Response:

Processes response  of the form:
{
    "count": 1, 
    "title": null, 
    "timestamp": 1313789630, 
    "uri": "http://services.digg.com/2.0/story.getTopNews?appkey=2788b5db0429e01726e233ba59a7d287&topic=&limit=1", 
    "cursor": "20110819164053:3bf4f568-f72b-4104-9fea-53013e715747", 
    "version": "2.0", 
    "stories": [
        {
            "status": "top", 
            "permalink": "http://digg.com/news/politics/jon_stewart_on_christians_pic", 
            "description": "One of many quotes by Jon Stewart on Christians", 
            "title": "Jon Stewart on Christians... (pic)", 
            "url": "http://uberhumor.com/jon-stewart-on-christians/", 
            "story_id": "20110819164053:3bf4f568-f72b-4104-9fea-53013e715747", 
            "diggs": 80, 
            "submiter": {
                "username": "THR", 
                "about": "The Hollywood Reporter (THR) is the premier destination and most-widely trusted resource for entertainment news, reviews, videos and analysis.\nPROMETHEUS GLOBAL MEDIA", 
                "user_id": "2687468", 
                "name": "The Hollywood Reporter", 
                "icons": [
                    "http://cdn1.diggstatic.com/user/2687468/c.png", 
                    "http://cdn2.diggstatic.com/user/2687468/h.png", 
                    "http://cdn1.diggstatic.com/user/2687468/m.png", 
                    "http://cdn1.diggstatic.com/user/2687468/l.png", 
                    "http://cdn3.diggstatic.com/user/2687468/p.png", 
                    "http://cdn1.diggstatic.com/user/2687468/s.png", 
                    "http://cdn3.diggstatic.com/user/2687468/r.png"
                ], 
                "gender": "", 
                "diggs": 60805, 
                "comments": 69, 
                "followers": 3269, 
                "location": "Hollywood, CA", 
                "following": 279, 
                "submissions": 970, 
                "icon": "http://cdn3.diggstatic.com/user/2687468/p.png"
            }, 
            "comments": 5, 
            "dugg": 0, 
            "topic": {
                "clean_name": "politics", 
                "name": "Politics"
            }, 
            "promote_date": 1313788859, 
            "activity": [], 
            "date_created": 1313772053, 
            "thumbnails": {
                "large": "http://cdn1.diggstatic.com/story/jon_stewart_on_christians_pic/l.png", 
                "small": "http://cdn2.diggstatic.com/story/jon_stewart_on_christians_pic/s.png", 
                "medium": "http://cdn3.diggstatic.com/story/jon_stewart_on_christians_pic/m.png", 
                "thumb": "http://cdn2.diggstatic.com/story/jon_stewart_on_christians_pic/t.png"
            }
        }
    ], 
    "authorized": 0, 
    "data": "stories", 
    "method": "story.getTopNews", 
    "user": ""
}
"""
