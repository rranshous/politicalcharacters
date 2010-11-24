import helpers as e # exceptions
import helpers as h
from templates import template_wrapper, TemplateArgs as targs, render
import helpers as e
from helpers import redirect, save_form_data, create_thumbnail, admin
import cherrypy
import models as m
from urllib2 import urlopen
import os.path

class Show:

    @cherrypy.expose
    def index(self):
        redirect('/show/list')

    @cherrypy.expose
    @template_wrapper('/shows/list.html')
    def list(self):
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
    def create(self,name=None,description=None,image=None,
                    image_url=None,action=None):
        if action:
            if not name:
                raise e.Validation('Name must be defined')

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

            show = m.Show(name=name,
                          description=description,
                          picture_path=os.path.basename(image_path))
            
            m.session.add(show)
            m.session.commit()
            redirect('/show/%s'%show.id)

class Character:

    @cherrypy.expose
    def index(self):
        redirect('/character/list')

    @cherrypy.expose
    @template_wrapper('/characters/list.html')
    def list(self):
        shows = m.Show.query.all()
        return targs(shows=shows)

    @cherrypy.expose
    @template_wrapper('/characters/single.html')
    def default(self,id):
        character = m.Character.get(id)
        if not character:
            raise e.Validation('Could not find character')
        return targs(character=character)

    @cherrypy.expose
    def vote(self,id,direction):
        character = m.Character.get(id)
        if not character:
            raise e.Validation('Could not find character')
        if direction.lower() == 'liberal':
            character.liberal_vote_count += 1
        elif direction.lower() == 'conservative':
            character.conservative_vote_count += 1
        else:
            raise e.Validation('What is %s?' % direction)
        character.total_vote_count += 1
        m.session.commit()
        redirect('/character/%s' % character.id)

    @cherrypy.expose
    def graph(self,id,**kwargs):
        cherrypy.log('graph: %s' % id)
        character = m.Character.get(id)
        if not character:
            raise e.Validation('Could not find character')
        src = render('/characters/graph.html',character=character).strip()
        return redirect(src)

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

class Thumbnail:

    @cherrypy.expose
    def default(self,img,size=200):
        cherrypy.log('thumbnail: %s' % img)
        # get the path
        image_root = cherrypy.config.get('image_root')
        thumbnail_root = cherrypy.config.get('thumbnail_root')
        path = create_thumbnail(os.path.join(image_root,img),
                                thumbnail_root,
                                size)
        path = os.path.abspath(path)
        # check and see if the thumbnail already exists
        cherrypy.log('thumbnail path: %s' % path)
        return cherrypy.lib.static.serve_file(path)

class Root:

    show = Show()
    character = Character()
    thumbnail = Thumbnail()

    @cherrypy.expose
    @template_wrapper('/index.html')
    def index(self):
        top_characters = m.Character.query. \
                            order_by(
                                m.Character.total_vote_count.desc()). \
                            limit(10).distinct().all()
        top_shows = m.Show.query.join('characters'). \
                            order_by( 
                                m.Character.total_vote_count.desc()). \
                            limit(10).distinct().all()
        return targs(top_characters=top_characters,
                     top_shows=top_shows)
