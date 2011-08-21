import web

from decimal import Decimal
import simplejson as json
import urllib
import httplib

#url_root = /farmville
urls = ( "/(.+)/(.+)/(.+)/?",  "Error",
         "/(.+)/(.+)/?",  "Api",
         "/?", "Docs",
         "/(.+)/?", "Error",)

#===============================================================#
# Api
#===============================================================#
class Docs:
    def GET(self):
        render = web.ctx.session['render']
        return render.apis()

class Api:
    def GET(self, service, query):
        """
        Serves all our APIs internally:
        /api/service/query or
        /api/service&ref=
        """
        web.header('Content-Type', 'text/plain')
        #web.header('Content-Type', 'application/json')
        if not query:
            i = web.input()
            query = i["ref"]
        self.service = service
        anon = getattr(self, "api_%s" % service, None)
        return anon(query)

    def api_exec(self, url):   
        try:
            response = urllib.urlopen(url)
            data = response.read().replace("$","")
            return data
        except:
            return None

    def api_youtube(self, query, dump=True):
        url = urllib.unquote("https://gdata.youtube.com/feeds/api/videos?alt=json&q=" + query.replace(" ", "+") + "&orderby=relevance&max-results=10&v2")
        data = json.loads(self.api_exec(url))["feed"]["entry"][0]["mediagroup"]["mediacontent"][0]['url']

        if dump:
            return json.dumps(data)
        return data

    def api_bing(self, query, sources="web"):
        url = urllib.unquote("http://api.search.live.net/json.aspx?Appid=38AF132A8C9243F6662C561D0890DDB2A5CA309C&query=" + query + "&sources=" + sources)
        return self.api_exec(url)
        #return json.loads()['SearchResponse']['Web']['Results'][0]

    def api_bing_image(self, query):
        return self.api_bing(query, sources="image")

    def api_bing_spell(self, query):
        return self.api_bing(query, sources="spell")

    def api_bing_phonebook(self, query):
        return self.api_bing(query, sources="phonebook")

    def api_bing_instant(self, query):
        return self.api_bing(query, sources="instantanswer")

    def api_ci(self, query):
        """API for complexityintelligence NLP"""        
        pass

    def api_embedly(self, query, width=150):
        api_key = "426ffa42c62711e0b9a74040d3dc5c07"
        url = "http://api.embed.ly/1/oembed?key=" + api_key + "&maxwidth=" + str(width) + "&urls=" + query
        return self.api_exec(url)

    def api_embedly_youtube(self, query):
        youtube = self.api_youtube(query, dump=False)
        e = json.loads(self.api_embedly(youtube))[0]
        data = {}
        data['html'] = e['html']
        data['thumb'] = e['thumbnail_url']
        data['url'] = e['url']
        return json.dumps(data)

    def api_box(self, query):
        api_key = "kjhtepcdg0hxdglfj7c0b23yszp7yc5v"
        pass

    def api_face(self, query):
        pass

    def api_envolve(self, query):
        #api_key = "FXMH7kyRM8Ffz95yZAGMu3DTkSvPKZY0"
        pass

    def api_zemanta(self, query):
        url = "http://api.zemanta.com/services/rest/0.0"
        params = urllib.urlencode({'api_key': "r8kdrptqrwbpgbtjr7pqappt",
                                   'method': 'jsonw',
                                   'text': query})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection(url)
        conn.request("POST", "", params, headers)
        data = conn.getresponse().read()
        conn.close()
        return data


#===============================================================#
# Error
#===============================================================#
class Error:
    def GET(self, service, data, error):
        """
        """
        return "404 - Congratulations! You got 2, 200 OK responses and 4 bonus points!"

subapp = web.application(urls, globals())

