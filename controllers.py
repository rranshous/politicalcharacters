import helpers as e # exceptions
import helpers as h
from templates import template_wrapper, TemplateArgs as targs
import helpers as e
from helpers import redirect, save_form_data
import cherrypy
import models as m
from urllib2 import urlopen
import os.path

class Show:

    @cherrypy.expose
    @template_wrapper('/shows/list.html')
    def index(self):
        shows = m.Show.query.all()
        return targs(shows=shows)

    @cherrypy.expose
    @template_wrapper('/shows/single.html')
    def default(self,id):
        show = m.Show.get(id)
        if not show:
            raise e.Validation('Could not find show')
        return targs(show=show)

    @cherrypy.expose
    @template_wrapper('/shows/create.html')
    def create(self,name=None,description=None,action=None):
        if action:
            if not name:
                raise e.Validation('Name must be defined')
            show = m.Show(name=name,description=description)
            m.session.add(show)
            m.session.commit()
            redirect('/show/%s'%show.id)

class Character:

    @cherrypy.expose
    def index(self):
        redirect('/show/list')

    @cherrypy.expose
    @template_wrapper('/characters/single.html')
    def default(self,id):
        character = m.Character.get(id)
        if not character:
            raise e.Validation('Could not find character')
        return targs(character=character)

    @cherrypy.expose
    @template_wrapper('/characters/create.html')
    def create(self,name=None,show_id=None,description=None,
                    image=None,image_url=None,action=None):

        if action:
            if not name:
                raise e.Validation('Name required')
            if not show_id:
                raise e.Validation('Show required')
            if not description:
                raise e.Validation('Description required')
            show = m.Show.get(show_id)
            if not show:
                raise e.Validation('Show not found')


            if image is not None and len(image.filename):
                cherrypy.log('has image: %s' % image.filename)
                image_path = save_form_data(image,
                                            cherrypy.config.get('image_root'),
                                           'character_')
            elif image_url:
                cherrypy.log('has image url')
                try:
                    image_path = _save_form_data(urlopen(image_url).read(),
                                            cherrpy.config.get('image_root'),
                                            image_url.rsplit('.',1)[-1],
                                            'character_')
                except:
                    cherrypy.log('bad download')
                    image_path = None

            else:
                image_path = None

            cherrypy.log("image_path: %s" % image_path)

            character = m.Character(name=name,
                                    show=show,
                                    description=description,
                                    picture_path=os.path.basename(image_path))
            m.session.add(character)
            m.session.commit()
            redirect('/character/%s' % character.id)

        return targs(shows=m.Show.query.all())

class Root:

    show = Show()
    character = Character()

    @cherrypy.expose
    @template_wrapper('/index.html')
    def index(self):
        return
