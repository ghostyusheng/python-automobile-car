import numpy as np

class Math:

    @classmethod
    def twristAngleToTwristTime(cls, V, R, angle):
        """
        simply change twrist angle problem to twrist time problem(differential wheels)
        """
        #V = velocity, angle = twristAngle, R = radius
        L = distance = 0
        W = anglespeed = 0
        W = (float)(2 * V) / R
        V = W * R
        L = (2 * np.pi * R) / 360 * angle
        T = L / V
        return T
