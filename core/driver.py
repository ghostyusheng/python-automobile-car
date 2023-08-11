import os 
import pigpio
from common.serial import Serial as S
from core.const import const
from util.function import pulseAcallback, pulseBcallback

class Driver:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def initSpeedWatcher(self):
        const.speedA = 0
        const.speedB = 0
        const.countA = 0
        const.countB = 0
        const.start_time1 = -1
        const.stop_time1 = -1
        const.start_time2 = -1
        const.stop_time2 = -1

        const.pi.callback(S.AENC1, pigpio.RISING_EDGE, pulseAcallback)
        const.pi.callback(S.BENC1, pigpio.RISING_EDGE, pulseBcallback)

    def init(self):
        """
        auto register 'sudo pigpiod' command by simple shell script tricks.
        """
        os.system("""
            if pgrep pigpiod;
                then echo ' <= SHELL => Exist pigpiod, not need to boot <= SHELL =>';
                else
                    sudo pigpiod && sleep 1 && echo '<= SHELL => Auto booting pigpiod <= SHELL =>'
            fi;""")
        const.pi = pigpio.pi()
        const.pi.write(S.STBY, 1)
        const.motion = None
        self.initSpeedWatcher()
