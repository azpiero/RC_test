# -*- coding: utf-8 -*-

from  BMX055 import BMXdata
import smbus2 as smbus
import time
import os
import sys
import GPS
import threading
from datetime import datetime
from contextlib import closing
import socket
import json
import calibration
import math
#import iothub_client

# 第一引数 dt 第二引数 IPAddress
if __name__ == '__main__':
    gpsthread = threading.Thread(target=GPS.rungps,args=())
    gpsthread.daemon = True
    gpsthread.start()
    b = BMXdata()
    dt = float(param[1])

    #s = socket.socket()
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = host = param[2]
    port = 5000

    with closing(client):
        deg_x = 0
        deg_y = 0
        deg_z = 0
        pgyrox = 0
        pgyroy = 0
        pgyroz = 0
        while 1 :
            #GPS
            gpsdata = GPS.getGPS()
            #sensor1
            acceldata = b.getAccel()
            gyrodata = b.getGyro()
            magdata = b.getMag()

            #deg_x += (pgyrox + gyrodata[0]/262.4)*dt/2
            #deg_y += (pgyroy + gyrodata[1]/262.4)*dt/2
            #deg_z += (pgyroz + gyrodata[2]/262.4)*dt/2

            #z軸回転（yaw回転）分の移り変わりを加味します
            #deg_x +=deg_y * math.sin(gyrodata[2]/262.4*dt*math.pi/180)
            #deg_y -=deg_x * math.sin(gyrodata[2]/262.4*dt*math.pi/180)


            result ={
                    "timeStamp" : datetime.now().strftime("%Y/%m/%d %H:%M:%S.")+"%03d" % (now.microsecond//1000) ,
                    "boatNumber": "1",
                    "position": {
                        "longitude": gpsdata[0],
                        "latitude": gpsdata[1]
                        },
                    "accelaration": {
                        #+-2g => 1LSBを1024段階で評価
                        #"x": acceldata[0]/1024,
                        #"y": acceldata[1]/1024,
                        #"z": acceldata[2]/1024
                        "x": acceldata[0],
                        "y": acceldata[1],
                        "z": acceldata[2]
                        },
                    "angular": {
                        #+-125 =>1LSBを262.4で評価
                        #"x": deg_x*0.9 + 0.1*calibration.degxbyaccel(acceldata[1]/1024,acceldata[2]/1024),
                        #"y": deg_y*0.9 + 0.1*calibration.degybyaccel(acceldata[0]/1024,acceldata[1]/1024,acceldata[2]/1024),
                        #"z": deg_z
                        "x": gyrodata[0],
                        "y": gyrodata[1],
                        "z": gyrodata[2]
                        },
                    "direction": {
                        "x": magdata[0],
                        "y": magdata[1],
                        "z": magdata[2]
                        }
                    }

            #pgyrox = gyrodata[0]/262.4
            #pgyroy = gyrodata[1]/262.4
            #pgyroz = gyrodata[2]/262.4

            client.sendto(str.encode(json.dumps(result)),(host,port))
            time.sleep(dt)
