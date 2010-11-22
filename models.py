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
    description = Field(UnicodeText)
    total_vote_count = Field(Integer, default=0)
    liberal_vote_count = Field(Integer, default=0)
    conservative_vote_count = Field(Integer, default=0)
    position = Field(Integer, default=0) # for list orderinga
    picture_path = Field(UnicodeText)

    def get_liberal_percent(self):
        if not self.liberal_vote_count:
            return 0
        return int(
                float(self.liberal_vote_count) / self.total_vote_count * 100)

    liberal_percent = property(get_liberal_percent)

    def get_conservative_percent(self):
        if not self.conservative_vote_count:
            return 0
        return int(
                float(self.conservative_vote_count) / self.total_vote_count
                * 100)

    conservative_percent = property(get_conservative_percent)


    show = ManyToOne('Show')

