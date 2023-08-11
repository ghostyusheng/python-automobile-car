import time
from util.function import *
from service.math import Math

class Automobile:

    @classmethod
    def stuckHandler(cls):
        """
            handle stuck situation of car, sometimes car stuck at blind angles.(repetitive turn left and turn right)
            first, set a threshold of cycle(repetitive turn left and turn right), if axceed the threshold, then force 
            turn left or right to avoid stuck.
        """
        const.stuckTolerance = 0
        const.lastFrontDistance = float('inf')
        while 1:
            if not const.RUN:
                continue
            if abs(const.frontDistance - const.lastFrontDistance < 0.2):
                print('const.frontDistance const.lastfrontDistance', const.frontDistance, const.lastFrontDistance)
                const.stuckTolerance += 1
                if const.stuckTolerance > 5:
                    const.RUN = 0
                    print('xxx --> stuck ! retreating !')
                    back()
                    time.sleep(2)
                    left()
                    time.sleep(2)
                    const.RUN = 1
                    const.stuckTolerance = 0
            const.lastFrontDistance = const.frontDistance
            time.sleep(6)


    @classmethod
    def movingTowardsColor(cls):
        """
        literally moving towards color, obsoleted now 
        """
        const.RUN = 0
        print(f'--> moving towards color:[{const.detectedVitalColor}]')
        blink(10, 0.1)
        current_color = const.detectedVitalColor._name
        print(type(current_color))
        if getattr(const, 'runed', None):
            print('runed!')
            return
        for i in range(10):
            print(f'--> 360 searching...current:[{current_color}], detect:[{const.detectedVitalColor._name}]')
            #T = Math.twristAngleToTwristTime(0.09708, 0.105, 10)
            right()
            time.sleep(3)
            if const.detectedVitalColor._name != current_color:
                print('---> 360 search higher proximity color success ! moving !')
                OFF()
                break
        OFF()
        const.runed = 1
        #const.RUN = 1


    @classmethod
    def prepareForword(cls):
        if not const.circumnavigated:
            return True
        if not const.detectedVitalColor:
            return True
        cls.movingTowardsColor()

    
    @classmethod
    def circumnavigate(cls, target_distance):
        const.RUN = 0
        print('--> start circumnavigate')
        blink(5)
        ON()
        T = Math.twristAngleToTwristTime(0.09708, 0.105, 30)

        if const.shakeCycleCount > 5:
            const.shakeCycleCount = 0
            const.shakeTolerance += 8
        if const.shakeTolerance > 0:
            right()
            const.shakeTolerance -= 1
        elif const.leftDistance < const.rightDistance:
            back()
            sleep(0.5)
            right()
            if const.LEFT == const.lastShakeDirection:
                const.shakeCycleCount += 1
                const.lastShakeDirection = const.RIGHT
        else:
            back()
            sleep(0.5)
            left()
            if const.RIGHT == const.lastShakeDirection:
                const.shakeCycleCount += 1
                const.lastShakeDirection = const.LEFT
        print('shake: ', const.shakeCycleCount)
        print('last shake: ', const.lastShakeDirection)
        time.sleep(T)
        #ON()
        OFF()
        const.RUN = 1
        const.circumnavigated = 1

    @classmethod
    def adjustDirection(cls, which_wheel):
        const.RUN = 0
        blink(5, 1)
        print(f'--> {which_wheel} detected block ! start adjust direction !')
        if which_wheel == 'right':
            left()
        elif which_wheel == 'left':
            right()
        time.sleep(1)
        OFF()
        const.RUN = 1
