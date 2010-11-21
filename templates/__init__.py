from mako.template import Template
from mako.lookup import TemplateLookup
import helpers as e
from helpers import add_flash
import helpers as h
import cherrypy
import os

from decorator import decorator

here = os.path.abspath(os.path.dirname(__file__))
lookup = TemplateLookup(directories=[here],format_exceptions=True,
                        output_encoding='utf-8', encoding_errors='replace')

def render(path,**kwargs):
    global errors, warnings, info, lookup
    template = lookup.get_template(path)
    cherrypy.log('request: %s' % cherrypy.request)
    kwargs.update({'session':cherrypy.session,
                   'request':cherrypy.request,
                   'h':h})
    s = template.render_unicode(**kwargs)
    return s




# we need a place holder for returning args to pass
# to the template
class TemplateArgs(dict):
    pass

def template_wrapper(path):
    """ returns decoartor which renders the passed path
        using the render function, passing to it the args
        which get returned to it """
    @decorator
    def template(f,*args,**kwargs):
        try:
            cherrypy.log('path: %s' % path)
            r = f(*args,**kwargs)
            if r:
                return render(path,**r)
            else:
                return render(path)
        except e.Validation, ex:
            add_flash('error','%s' % ex)
    return template

