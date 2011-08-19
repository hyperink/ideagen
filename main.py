import web
import urllib
import simplejson as json
from apis.pyGTrends import pyGTrends
#from subapps import api_app as api_app

GLOBALNAME = "Hyperink Trends"

web.config.debug == True

if web.config.debug:
    from reloader import PeriodicReloader

# url mapping
urls = (
    '/?',               "Index", #weseeyou_app.subapp,
    '/(.*)',            "Error",
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
        return render.index()

    def POST(self):
        i = web.input()
        usr = i['google_username']
        pwd = i['google_password']
        kwarg1 = i['kwarg1']
        kwarg2 = i['kwarg2']
        connector = pyGTrends(usr, pwd)
        connector.download_report((kwarg1, kwarg2))        
        return render.index(connector.csv())

class Error:
    def GET (self, err):
        return "<h1>404 - Congratulations!</h1><p>You got 2, <span style='color: green;'>200 OK</span> responses and 4 bonus points!</p><img src='http://generationbass.com/wp-content/uploads/2009/09/Results-winner.jpg' width=175 />"

if __name__ == "__main__":
    if web.config.debug:
        PeriodicReloader()
    app.run()
