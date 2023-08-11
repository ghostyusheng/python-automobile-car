from rplidar import RPLidar
import math
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians, pi

"""
lidar debuging script, still working on it now.
"""

serial = '/dev/ttyUSB0'

lidar = RPLidar(serial)

info = lidar.get_info()
print('info:', info)

health = lidar.get_health()
print('health:', health)
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
#
#l = np.array([0, 0, 0])
#for i, scan in enumerate(lidar.iter_scans()):
#    print('%d: Got %d measurments' % (i, len(scan)))
#    #print(scan, type(scan))
#    l = np.vstack([l, np.array(scan)])
#    #break
#    if i > 10:
#        break
#
#
#l[:,2] = l[:,2] / 10
#l = l.astype(int)
#l = np.unique(l, axis=1)
#
#xyreso = 0.3  # x-y grid resolution
#yawreso = math.radians(3.1)  # yaw angle resolution [rad]
#ang = l[:,1]
#dist = l[:,2]
#ox = np.sin(ang) * dist
#oy = np.cos(ang) * dist
#print(ox, oy)
#
#plt.figure(figsize=(6,10))
#plt.plot([oy, np.zeros(np.size(oy))], [ox, np.zeros(np.size(oy))], "ro-") # lines from 0,0 to the
#plt.axis("equal")
#bottom, top = plt.ylim()  # return the current ylim
#plt.ylim((top, bottom)) # rescale y axis, to match the grid orientation
#plt.grid(True)
#plt.show()
#
#
#lidar.stop()
#lidar.stop_motor()
#lidar.disconnect()
#
