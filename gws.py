#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gws.server import server, requestHandler

def init():
    server_address = ('0.0.0.0', 8081)
    httpd = server(server_address, requestHandler)
    return httpd

def run(httpd):
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access

    
    print('running server...')
    httpd.serve_forever()

def shutdown(httpd):
    httpd.cleanup()
    httpd.shutdown()

httpd = init()

try:
    run(httpd)
except (KeyboardInterrupt, SystemExit):
    shutdown(httpd)
