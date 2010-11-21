import helpers as e # exceptions
import helpers as h
from templates import template_wrapper, TemplateArgs as targs
import helpers as e
from helpers import redirect
import cherrypy
import models as m

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
            redirect('/shows/%s'%show.id)

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
    @template_wrapper('/characters/new.html')
    def create(self,name=None,show_id=None,description=None,action=None):
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

            character = m.Character(name=name,
                                    show=show,
                                    description=description)
            m.session.add(character)
            m.session.commit()
            redirect('/character/%s' % character.id)

class Root:

    show = Show()
    character = Character()

    index = show.index
