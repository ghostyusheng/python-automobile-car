from util.function import *
from service.math import Math
from service.sensor import Sensor

class Control:

    @classmethod
    def keybordControl(cls):
        """
        async control vehicle by keyboard(even the car is controling by the algorithm),
        you can stop car whenever you want to check debug log and update algorithm
        """
        setDutycycleAndFrequency(100, 100)
        print('=> wasd control')
        while(1):
            i = input()
            if i=='w':
                forward()
            elif i=='s':
                back()
            elif i=='d':
                right()
            elif i=='a':
                left()
            elif i=='f':
                OFF()
            elif i=='g':
                ON()
            elif i=='1':
                OFF()
                T = Math.twristAngleToTwristTime(0.09708, 0.105, 5)
                HIGH('AIN2'), LOW('AIN1')
                LOW('BIN2'), HIGH('BIN1')
                setDutycycleAndFrequency('left', 30)
                setDutycycleAndFrequency('right', 30)
                ON()
                import time
                end = time.time() + T + 0.1
                _t = time.time()
                while _t < end:
                    _t = time.time()
                OFF()
            else:
                print('command not found \n')
