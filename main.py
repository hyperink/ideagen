import web
import urllib2
import json
from apis.pyGTrends import pyGTrends
#from subapps import api_app as api_app

GLOBALNAME = "Hyperink Trends"

APIs = { 'wtt': { 'key': "28ba654d201927880ddc845a8e82eae23cffd9de",
                  'url': "http://api.whatthetrend.com/api/v2/trends.json"},
         'digg': {'key': '',
                  'url': ''},
         }
web.config.debug == True

if web.config.debug:
    from reloader import PeriodicReloader

# url mapping
urls = (
    '/?',    "Index", #weseeyou_app.subapp,
    '/(.*)', "Error",
    )

app = web.application(urls, globals())

# global vars
the_globals = { 'ctx': web.ctx,
                'globalname': GLOBALNAME,
                }

render = web.template.render('templates/',
                             base='layout',
                             globals=the_globals)

slender = web.template.render('templates/',
                              globals=the_globals)

the_globals['render'] = render
the_globals['slender'] = slender

def session_hook():
    web.ctx.session = { "render": render,
                        "slender": slender,
                        }

app.add_processor(web.loadhook(session_hook))

class Index:
    def GET(self):
        """
        When a GET request is made to the url caught by regex pattern "/"
        Then serve the index page from ideagen/templates
        """
        return render.index()

    def POST(self):
        """
        Use the information provided by the user to do a Google Trends search
        or retrieve trends as JSON using "What The Trend's" REST API.
        """
        i = web.input()
        trends = {}
        for key in APIs:
            callback = getattr(i, key, None)
            if callback:
                trends[key] = getattr(self, 'get_' + key +'_trends', None)()
                 
        #trends = self.get_wtt_trends()
        #self.get_google_trends(i)
        return render.index(trends)

    def get_wtt_trends(self, getJSON=True):
        api_key = APIs['wtt']['key']
        url = APIs['wtt']['url']
        data = urllib2.urlopen(url).read()
        if getJSON:
            data = json.loads(data)
        return data

    def get_google_trends(self, i):
        usr = getattr(i, 'google_username', None)
        pwd = getattr(i, 'google_password', None)
        kwarg1 = getattr(i, 'kwarg1', None)
        kwarg2 = getattr(i, 'kwarg2', None)
        connector = pyGTrends(usr, pwd)
        connector.download_report((kwarg1, kwarg2))        
        return render.index(connector.csv())

class Error:
    """
    This class will handle all unmatched URL requests as 404 errors
    """
    def GET (self, err):
        return "<h1>404 - Congratulations!</h1><p>You got 2, <span style='color: green;'>200 OK</span> responses and 4 bonus points!</p><img src='http://generationbass.com/wp-content/uploads/2009/09/Results-winner.jpg' width=175 />"

if __name__ == "__main__":
    if web.config.debug:
        PeriodicReloader()
    app.run()
