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
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult, IoTHubError

CONNECTION_STRING = "HostName=Motorboat-Hub.azure-devices.net;DeviceId=Takeru-Mac;SharedAccessKey=stLFEtWUyghJPugEl59ATtIlkinBuQKSJLgHII2t0Uc="
PROTOCOL = IoTHubTransportProvider.HTTP

def blob_upload_conf_callback(result, user_context):
    if str(result) == 'OK':
        print ( "...file uploaded successfully." )
    else:
        print ( "...file upload callback returned: " + str(result) )

def iothub_file_upload_sample_run():
    try:
        print ( "IoT Hub file upload sample, press Ctrl-C to exit" )

        client = IoTHubClient(CONNECTION_STRING, PROTOCOL)

        b = BMXdata()
        gpsdata = GPS.getGPS()
        acceldata = b.getAccel()
        gyrodata = b.getGyro()
        magdata = b.getMag()

        content = json_string ={
                    "timeStamp" : datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    "boatNumber": "3",
                    "position": {
                        "longitude": gpsdata[0],
                        "latitude": gpsdata[1]
                        },
                    "accelaration": {
                        "x ": acceldata[0],
                        "y": acceldata[1],
                        "z": acceldata[2]
                        },
                    "angular": {
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

        client.upload_blob_async("test", content, len(content), blob_upload_conf_callback, 0)

        print ( "" )
        print ( "File upload initiated..." )
        while True:
            time.sleep(30)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
    except: 
        print ( "generic error" )

if __name__ == '__main__':
    gpsthread = threading.Thread(target=GPS.rungps,args=())
    gpsthread.daemon = True
    gpsthread.start()
    #b = BMXdata()
    iothub_file_upload_sample_run()
    #s = socket.socket()
    #client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #host = "192.168.11.2"
    #port = 5000

    #with closing(client):
    #    while 1 :

