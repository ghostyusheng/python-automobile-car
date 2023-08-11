#!/usr/bin/python3

from util.function import *
from core.driver import Driver
from service.control import Control
from service.sensor import Sensor


def main():
    Driver().init()
    const.DEBUG = 1
    const.RUN = 0
    regStopEvent()
    OFF()
    Sensor.listening()
    Control.keybordControl()

if __name__ == '__main__':
    main()

