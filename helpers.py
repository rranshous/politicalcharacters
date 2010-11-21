import cherrypy
from cherrypy import HTTPRedirect, HTTPError


def add_flash(msg_type,msg=None):
    if not msg:
        msg = msg_type
        msg_type = 'info'

    cherrypy.session.setdefault(msg_type,[]).append(msg)

def redirect(*args,**kwargs):
    raise HTTPRedirect(*args,**kwargs)

class Validation(Exception):
    pass

