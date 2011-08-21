import web
import json
from apis import wtt
from apis import google
#from subapps import middleware_app
#from apis import digg_api
import digg_api as digg
from collections import defaultdict

#from subapps import api_app as api_app

GLOBALNAME = "Hyperink Trends"

APIs = { 'wtt': { 'key': "28ba654d201927880ddc845a8e82eae23cffd9de",
                  'url': "http://api.whatthetrend.com/api/v2/trends.json"},
         'digg': {'key': '',
                  'url': ''},
         'google': {'key': '',
                    'url': ''},         
         }

web.config.debug == True

if web.config.debug:
    from reloader import PeriodicReloader

# url mapping
urls = (
#    '/api',  middleware_app.subapp,
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
                api_key = APIs[key]['key']
                api_url = APIs[key]['url']

                if key == "digg":
                    trends[key] = digg.get_corpus()
                else:
                    trends[key] = getattr(globals()[key], 'get_' + key +'_trends', None)(i, api_key=api_key, api_url=api_url)

        #trends = self.get_wtt_trends()
        #self.get_google_trends(i)
        return render.index(trends)

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
