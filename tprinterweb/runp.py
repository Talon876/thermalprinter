#!/usr/bin/env python
import cherrypy
from app import app
from config import PORT

cherrypy.tree.graft(app, '/')
cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': PORT,
})
cherrypy.engine.start()
cherrypy.engine.block()

