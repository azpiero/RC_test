import math

def degybyaccel(accelx,accely,accelz):
    return -math.atan2(accelx,math.sqrt(accely*accely+accelz*accelz)) * math.pi/180

def degxbyaccel(accely,accelz):
    return -math.atan(accely/accelz)
            


