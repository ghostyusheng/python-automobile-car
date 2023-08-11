import threading
import time
import dependency.GP2Y as GP2Y
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
from service.automobile import Automobile
from service.vision import Vision
from util.function import *
from core.const import const

class Sensor(threading.Thread):
    """
    provide a class to register async functions.
    async sensors: proximity, camera, ultrasonic sensors
    async function: log_debug(output/s), stuck_detector(handle blind angle), speed_watch(asyc update speed)
    """
    def __init__(self, threadID, name, whichHandler):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.handler = whichHandler

    def run(self):
        print("Starting " + self.name)
        if self.handler == 'proximity':
            self.settingProximitySensor()
        elif self.handler == 'camera':
            self.settingCameraSensor()
        elif self.handler == 'ultrasonic_sensor_left':
            self.settingUltrasonicSensor('left')
        elif self.handler == 'ultrasonic_sensor_right':
            self.settingUltrasonicSensor('right')
        elif self.handler == 'log_debug':
            self.log()
        elif self.handler == 'stuck_detector':
            self.stuckHandler()
        elif self.handler == 'speed_watcher':
            self.speedWatcher()
        print("Exiting " + self.name)


    @classmethod
    def speedWatcher(cls):
        while 1:
            _time1 = _time2 = 0
            wheel_circumference = 47 * np.pi
            counter_dis = wheel_circumference/(298*6)
            dist_A = const.countA * counter_dis
            dist_B = const.countB * counter_dis
            _time1 = (const.stop_time1 - const.start_time1)/1000000
            _time2 = (const.stop_time2 - const.start_time2)/1000000
            const.start_time1 = -1
            const.stop_time1 = -1
            const.start_time2 = -1
            const.stop_time2 = -1
            if _time1:
                const.speedA = dist_A/_time1/10 
            if _time2:
                const.speedB = dist_B/_time2/10
            const.countA = 0
            const.countB = 0
            #print(dist_A, dist_B, counter_dis)
            time.sleep(2)

    @classmethod
    def stuckHandler(cls):
        Automobile.stuckHandler()

    @classmethod
    def log(cls):
        while 1:
            color =  getattr(getattr(const, 'detectedVitalColor', None), '_name', None)
            if hasattr(const, 'frontDistance') and hasattr(const, 'leftDistance') and hasattr(const, 'rightDistance'):
                print(f"left,front,right(cm): [{color}] {const.leftDistance:.1f} <- {const.frontDistance:.1f} -> {const.rightDistance:.1f}")
            print(f"speed(cm/s): {const.speedA:.1f} <--> {const.speedB:.1f}")
            print(const.motion)
            print(f"encoder: {const.countA}, {const.countB}")
            time.sleep(1)

    @classmethod
    def settingCameraSensor(cls):
        Vision().preBoot().framesHandler()


    @classmethod
    def settingProximitySensor(cls):
        const.circumnavigated = 0
        while True:
            GP2Y.distcalc()
            L = GP2Y.Distance
            const.frontDistance = L
            if L < 15:
                const.RUN and Automobile.circumnavigate(L)
                pass
            else:
                #const.RUN and Automobile.prepareForword() and forward()
                const.RUN and forward()
                pass
            time.sleep(0.1)

    @classmethod
    def getUltrasonicSensorDistance(cls, GPIO_TRIGGER, GPIO_ECHO):
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        return distance

    @classmethod
    def settingUltrasonicSensor(cls, which_wheel):
        GPIO.setmode(GPIO.BCM)
        if which_wheel == 'left':
            GPIO_TRIGGER = S.TRIGER2
            GPIO_ECHO = S.ECHO2
        elif which_wheel == 'right':
            GPIO_TRIGGER = S.TRIGER1
            GPIO_ECHO = S.ECHO1
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        const.shakeCycleCount = 0
        const.lastShakeDirection = const.LEFT
        const.shakeTolerance = 0
        const.lastLeftDistance = -1
        const.lastRightDistance = -1
        while True:
            try:
                dist = cls.getUltrasonicSensorDistance(GPIO_TRIGGER, GPIO_ECHO)
                wheel = which_wheel + "Distance"
                setattr(const, wheel, dist)
                if dist < 12:
                    const.RUN and Automobile.adjustDirection(which_wheel)
                setattr(const, 'last' + wheel.capitalize(), dist)
            except Exception as e:
                print(e)
            time.sleep(0.1)


    @classmethod
    def listening(cls):
        thread0 = cls(99, 'log_debug', 'log_debug')
        thread1 = cls(1, 'thread_proximity_sensor',  'proximity')
        thread2 = cls(2, 'thread_camera_sensor', 'camera')
        thread3 = cls(3, 'thread_ultrasonic_sensor_left', 'ultrasonic_sensor_left')
        thread4 = cls(4, 'thread_ultrasonic_sensor_right', 'ultrasonic_sensor_right')
        thread5 = cls(5, 'stuck_detector', 'stuck_detector')
        thread6 = cls(6, 'speed_watcher', 'speed_watcher')
        thread0.start()
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
