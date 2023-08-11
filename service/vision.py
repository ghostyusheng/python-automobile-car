import time
import cv2
import picamera
import picamera.array
from common.color import *
from cv2 import aruco
from core.const import const
from util.function import *

class Vision:
    """
    camera frames handler class:
        1.identify arucoCode 
        2.classify color and shape of color
    """
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.aruco_parameters = aruco.DetectorParameters_create()

    def preBoot(self):
        """
        pre boot configures of camera
        """
        camera = picamera.PiCamera()
        camera.rotation = 180
        camera.resolution = (600, 480)
        camera.framerate = 32
        self.camera = camera
        self.rawCapture = picamera.array.PiRGBArray(camera, size=camera.resolution)
        time.sleep(0.1)
        return self

    def framesHandler(self):
        const.detectedVitalColor = None
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            self.img = frame.array
            exitCode1 = self.colorIdentify()
            exitCode2 = self.arucoIdentity()
            if -1 in (exitCode1, exitCode2):
                break
            time.sleep(0.5)

    def arucoIdentity(self):
        """
        async identify aruco code
        """
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        corners,ids,rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_parameters)
        
        frame_markers = aruco.drawDetectedMarkers(self.img, corners, ids)
        winname = "arucoIdentity"
        cv2.namedWindow(winname)        # Create a named window
        cv2.moveWindow(winname, 0,500)  # Move it to (40,30)
        cv2.imshow(winname, frame_markers)
        self.rawCapture.truncate(0)
        try:
            ids = ids.tolist()
        except Exception as e:
            ids = []
        if ids and len(ids):
            print('detected id: ', ids)
            color =  getattr(getattr(const, 'detectedVitalColor', None), '_name', None)
            if [4] in ids and color == 'green' and const.frontDistance < 25:
                print('---> Goal!!!')
                const.RUN = 0
                OFF()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return -1
        
    def setColor(self):
        """
        async update color that camera captured, and save into const instance
        """
        img = self.img
        hsv = const.hsv
        for color_obj in color_sequence:
            color = color_obj._name
            mask = cv2.inRange(hsv, color_obj.hsvMin, color_obj.hsvMax)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            threshold = 100
            for c in contours:
                perimeter = cv2.arcLength(c, True)
                if perimeter < threshold:
                    continue
                if not const.detectedVitalColor:
                    const.detectedVitalColor = color_obj
                else:
                    priorityNewColor = color_sequence.index(color_obj) 
                    priorityCurrentColor = color_sequence.index(const.detectedVitalColor) 
                    if priorityNewColor > priorityCurrentColor:
                        print(f'--> find priority color, update [{const.detectedVitalColor._name}] -> [{color_obj._name}]!')
                        const.detectedVitalColor = color_obj
                img = cv2.drawContours(img, [c], -1, (0,255,255), 3)
       

    def colorIdentify(self):
        img = self.img
        self.frame_count += 1
        average_fps = self.frame_count / ( time.time() - self.start_time )
        const.hsv = hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        (const.frontDistance < 20) and self.setColor()
        cv2.imshow("colorIdentity", img)
        self.rawCapture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return -1
