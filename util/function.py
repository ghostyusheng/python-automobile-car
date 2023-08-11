import atexit
import time
import threading
import RPi.GPIO as GPIO
from common.serial import Serial as S
from core.const import const

"""
provide some basic functions to let programmers focus on the business, not pins.
"""

def HIGH(serial, log=False):
    sid = getattr(S, serial)
    log and const.DEBUG and print(f'==> {serial}({sid}) -> 1')
    const.pi.write(sid, 1)

def LOW(serial, log=False):
    sid = getattr(S, serial)
    log and const.DEBUG and print(f'==> {serial}({sid}) -> 0')
    const.pi.write(sid, 0)

def ON():
    const.DEBUG and print(f'==> PWM ON')
    LOW('AIN2'), HIGH('AIN1')
    LOW('BIN2'), HIGH('BIN1')

def OFF():
    const.DEBUG and print(f'==> PWM OFF')
    HIGH('AIN2'), HIGH('AIN1')
    HIGH('BIN2'), HIGH('BIN1')
    const.motion = 'stop'

def forward():
    setDutycycleAndFrequency('all', 100)
    LOW('AIN2'), HIGH('AIN1')
    LOW('BIN2'), HIGH('BIN1')
    const.motion = 'forward'

def back():
    setDutycycleAndFrequency('all', 100)
    HIGH('AIN2'), LOW('AIN1')
    HIGH('BIN2'), LOW('BIN1')
    const.motion = 'back'

def right():
    setDutycycleAndFrequency('left', 100)
    setDutycycleAndFrequency('right', 100)
    HIGH('AIN1'), LOW('AIN2')
    LOW('BIN1'), HIGH('BIN2')
    const.motion = 'right'

def left():
    setDutycycleAndFrequency('left', 100)
    setDutycycleAndFrequency('right', 100)
    HIGH('AIN2'), LOW('AIN1')
    LOW('BIN2'), HIGH('BIN1')
    const.motion = 'left'

"""
blink the light, is one of the signal help to debug your algorithm
"""
def blink(times, interval=0.1):
    print('start blinking')
    const.pi.set_mode(S.LED, 1)
    def say(times):
        for i in range(0,times):
            HIGH('LED', False)
            time.sleep(interval)
            LOW('LED', False)
            time.sleep(0.1)
    t = threading.Thread(target=say, args=(times,))
    t.start()

def setDutycycleAndFrequency(wheel, dutycycle=100,frequency=100):
    if wheel == 'left':
        const.pi.set_PWM_dutycycle(S.PWMA, dutycycle)
        const.pi.set_PWM_frequency(S.PWMA, frequency)
    elif wheel == 'right':
        const.pi.set_PWM_dutycycle(S.PWMB, dutycycle)
        const.pi.set_PWM_frequency(S.PWMB, frequency)
    elif wheel == 'all':
        const.pi.set_PWM_dutycycle(S.PWMA, dutycycle)
        const.pi.set_PWM_frequency(S.PWMA, frequency)
        const.pi.set_PWM_dutycycle(S.PWMB, dutycycle)
        const.pi.set_PWM_frequency(S.PWMB, frequency)


def pulseAcallback(gpio, level, tick):
    if level == 1:
        if const.start_time1 == -1:
            const.start_time1 = tick
            return
        const.stop_time1 = tick
        const.countA += 1
        #if const.motion in ('forward', 'right'):
        #    const.countA += 1
        #elif const.motion == 'stop':
        #    const.countA = 0
        #else:
        #    const.countA -= 1

def pulseBcallback(gpio, level, tick):
    if level == 1:
        if const.start_time2 == -1:
            const.start_time2 = tick
            return
        const.stop_time2 = tick
        if const.motion in ('forward', 'left'):
            const.countB += 1
        elif const.motion == 'stop':
            const.countB = 0
        else:
            const.countB -= 1

def sleep(i):
    time.sleep(i)

"""
release all opened resources when program stoped
"""
def regStopEvent():
    def _stopBeforeExit():
        const.pi.stop()
        GPIO.cleanup()
        print('==== Released all the pin protocal! ====')
    atexit.register(_stopBeforeExit)
