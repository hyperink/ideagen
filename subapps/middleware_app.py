"""
We're trying to avoid same origin policy
"""

import web
from decimal import Decimal
import simplejson as json
import urllib

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

    def api_googletrends(self, query=None, dump=True):
        """
        This module is not yet supported due to the fact that we are
        only using JSON and not XML
        """
        url = urllib.unquote("http://www.google.com/trends/hottrends/atom/hourly")
        data = json.loads(self.api_exec(url))
        if dump:
            return json.dumps(data)
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

