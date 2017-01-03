#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import ast

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gpios",  dest = "gpios", default = "[2,3,4]", help="List of gpios which shall be handled: -g=[1,2,3]")


args = parser.parse_args()

try:
    gpios = ast.literal_eval(args.gpios)
except:
    print("The argument --gpios="+str(args.gpios)+" is no list")
    exit(0)

if not isinstance(gpios, list):
    print("The argument --gpios="+str(args.gpios)+" is no list")
    exit(0)

import gws
from gws import web


def init():
    server_address = ('0.0.0.0', 8081)
    print('starting server...')
    httpd = web.server(server_address, web.requestHandler)
    return httpd

def run(httpd):
    print('running server...')
    httpd.serve_forever()

def shutdown(httpd):
    httpd.cleanup()
    httpd.shutdown()

httpd = init()


gws.gpio.set_gpios(gpios)
gws.gpio.reset()

try:
    run(httpd)
except (KeyboardInterrupt, SystemExit):
    shutdown(httpd)
