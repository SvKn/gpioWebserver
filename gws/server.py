#!/usr/bin/python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer

import RPi.GPIO as GPIO

class server(HTTPServer):

    def __init__(self, srv_adr, req_class):
        
        super(server, self).__init__(srv_adr, req_class)

        
        print("init server")

        self.gpio_pwms = {}
        self.init_gpios()

    def init_gpios(self):
        GPIO.setmode(GPIO.BCM)

        mode = GPIO.getmode()

        self.gpios = [2, 3, 4]

        GPIO.setwarnings(False)

        GPIO.setup(self.gpios, GPIO.OUT)
        GPIO.output(self.gpios, GPIO.LOW )

        # Create PWM for each GPIO
        for g in self.gpios:
            self.gpio_pwms[str(g)] =  GPIO.PWM(g, 1000)


        for i in self.gpio_pwms.keys():
            
            self.gpio_pwms[i].start(0)

    def adjust_duty_cycle(self, gpio, dc):
        self.gpio_pwms[str(gpio)].ChangeDutyCycle(float(dc))

    def gpio_on(self, gpio):
        self.gpio_pwms[str(gpio)].ChangeDutyCycle(100)

    def gpio_off(self, gpio):
        self.gpio_pwms[str(gpio)].ChangeDutyCycle(0)

    def cleanup(self):
        

        for i in self.gpio_pwms.keys():
            
            self.gpio_pwms[i].stop()


# HTTPRequestHandler class
class requestHandler(BaseHTTPRequestHandler):
    
    def __init__(self, request_client, client_address, server):
        
        super(requestHandler, self).__init__(request_client, client_address, server)
        
        #p.ChangeDutyCycle(50)

    # GET
    def do_GET(self):
        
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))

        req_path = self.path
        
        call = req_path.split('/')

        if (call[1] == "gpio" ):
            gpio  = call[2]
            com   = call[3]
            

            if (com == "pwm" ):
                dc    = call[4]
                self.server.adjust_duty_cycle(gpio, dc)

            if (com == "on" ):
                self.server.gpio_on(gpio)

            if (com == "off" ):
                self.server.gpio_off(gpio)

        return
