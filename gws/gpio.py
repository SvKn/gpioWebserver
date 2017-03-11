#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

class gpio():

    def __init__(self):

        self.gpio_pwms = {}
        self.gpios = []
        self.dc = {}

        GPIO.setmode(GPIO.BCM)
        mode = GPIO.getmode()

    def init_gpios(self):

        GPIO.setwarnings(False)

        GPIO.setup(self.gpios, GPIO.OUT)
        GPIO.output(self.gpios, GPIO.LOW )

        # Create PWM for each GPIO
        for g in self.gpios:
            self.gpio_pwms[str(g)] =  GPIO.PWM(g, 1000)

        for i in self.gpio_pwms.keys():          
            self.gpio_pwms[i].start(0)
            self.dc[i] = 0
        

    def set_gpios(self, gpios):
        self.gpios = gpios

    def reset(self):
        self.cleanup()
        self.init_gpios()

    def set_duty_cycle(self, gpio, dc):
        if gpio in self.gpio_pwms:
            self.gpio_pwms[str(gpio)].ChangeDutyCycle(float(dc))
            self.dc[gpio] = float(dc)

    def on(self, gpio):
        if gpio in self.gpio_pwms:
            self.gpio_pwms[str(gpio)].ChangeDutyCycle(100)
            self.dc[gpio] = 100

    def off(self, gpio):
        if gpio in self.gpio_pwms:
            self.gpio_pwms[str(gpio)].ChangeDutyCycle(0)
            self.dc[gpio] = 0


    def cleanup(self):

        for i in self.gpio_pwms.keys():
            self.gpio_pwms[i].stop()

        if not len(self.gpios):
            GPIO.cleanup()
            self.gpio_pwms = {}
            self.dc = {}

    def get_gpios(self):
        return self.gpios

    def get_state(self):
        print(self.gpios)
        print(self.dc)
        return dict(zip(self.dc.keys(), self.dc.values()))

    def get_state2(self):
        state = ''
        for i in sorted(self.gpio_pwms.keys()):
            state = state + "GPIO["+ str(i) + "] = " + str(self.dc[i]) + "</br> \n"

        return state
