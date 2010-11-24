#!/usr/bin/python

import cherrypy

import controllers as c
import models as m

import cherrypy.lib.auth_basic
pd = cherrypy.lib.auth_basic.checkpassword_dict

if __name__ == "__main__":
    # setup the db connection
    m.setup()

    # setup a tool to rset our db session
    cherrypy.tools.reset_db = cherrypy.Tool('on_end_resource',
                                            m.reset_session)

    # get this thing hosted
#    cherrypy.tree.mount(c.Root(), '/', config='./cherryconfig.ini')
    cherrypy.quickstart(c.Root(), '/', config='cherryconfig.ini')
