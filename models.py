from elixir import *
import cherrypy


def reset_session():
    try:
        session.rollback()
        session.expunge_all()
        session.remove()

    except:
        pass
    return

def setup():
    metadata.bind = "sqlite:///./dbs/production.db"
    metadata.bind.echo = False
    setup_all()


class Show(Entity):
    using_options(tablename='shows')

    name = Field(UnicodeText)
    description = Field(UnicodeText)
    picture_path = Field(UnicodeText)

    characters = OneToMany('Character')


class Character(Entity):
    using_options(tablename='characters')

    name = Field(UnicodeText)
    total_vote_count = Field(Integer)
    liberal_vote_count = Field(Integer)
    conservative_vote_count = Field(Integer)
    position = Field(Integer) # for list orderinga
    picture_path = Field(UnicodeText)

    show = ManyToOne('Show')

