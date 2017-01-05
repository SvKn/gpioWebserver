#!/usr/bin/python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer

import gws

import re
re_pwm = re.compile("^/gpio/(\d+)/pwm/([0-9]|[1-8][0-9]|9[0-9]|100)$")
re_num = re.compile("\d+")
re_on_off = re.compile("^/gpio/\d+/(on|off)$")
re_state = re.compile("(on|off)")

hyperlink_format = '<a href="http://192.168.0.105:8081/{link}">{text}</a>'

class server(HTTPServer):

    def __init__(self, srv_adr, req_class):
        
        super(server, self).__init__(srv_adr, req_class)

        print("init server")

    def adjust_duty_cycle(self, gpio, dc):
        gws.gpio.set_duty_cycle(gpio, dc)

    def gpio_on(self, gpio):
        gws.gpio.on(gpio)

    def gpio_off(self, gpio):
        gws.gpio.off(gpio)

    def cleanup(self):
        gws.gpio.cleanup()

    def get_state(self):
        return gws.gpio.get_state()


class requestHandler(BaseHTTPRequestHandler):
            
    def do_GET(self):
        
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = "Current GPIO State: </br>" + '\n'
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))

        req_path = self.path
        
        call = req_path.split('/')
        
        if re_pwm.match(self.path):
            m = re_num.findall(self.path)
            gpio  = m[0]
            dc    = m[1]
            self.server.adjust_duty_cycle(gpio, dc)

        if re_on_off.match(self.path):
            gpio = re_num.findall(self.path)
            new_state = re_state.findall(self.path)

            if (new_state[0] == "off" ):
                self.server.gpio_off(gpio[0])

            if (new_state[0] == "on" ):
                self.server.gpio_on(gpio[0])

        state = self.server.get_state()

        content = "</br>"
        for gpio in state:
            content = content + self.link_gpio_on(gpio)
            content = content + self.link_gpio_off(gpio)

        self.wfile.write(bytes(str(state), "utf8"))

        self.wfile.write(bytes(str(content), "utf8"))

        return

    def link_gpio_on(self, gpio):
        return create_link("gpio/" + str(gpio) +  "/on", str(gpio) + " -> on") + "</br>"

    def link_gpio_off(self, gpio):
        return create_link("gpio/" + str(gpio) +  "/off", str(gpio) + " -> off") + "</br>"

    def log_message(self, format, *args):
        pass
        return

def create_link(link, text):
    ahref = hyperlink_format.replace("{link}", link)
    ahref = ahref.replace("{text}", text)
    return ahref

