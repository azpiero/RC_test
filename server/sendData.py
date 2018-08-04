import time
import sys
import iothub_client
import os
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult, IoTHubError
import socket
from contextlib import closing
import sys

CONNECTION_STRING = "Motorboat-Hub.azure-devices.net;DeviceId=Takeru-Mac;SharedAccessKey=stLFEtWUyghJPugEl59ATtIlkinBuQKSJLgHII2t0Uc="

PROTOCOL = IoTHubTransportProvider.HTTP

#PATHTOFILE = "[Full path to file]"
#FILENAME = "[File name on storage after upload]"
{
    "BoatNumber": "3",
    "Position": {
        "longitude": "135.1",
        "latitude": "30.432"
    },
    "Accelaration": {
        "accelx ": "100",
        "accely": "200",
        "accelz": "300"
    },
    "Angular": {
        "x": "1",
        "y": "2",
        "z": "3"
    },
    "Direction": {
        "x": "10.1",
        "y": "20.2",
        "z": "30.3"
    },
    "Speed": {
        "x": "6",
        "y": "7",
        "z": "8"
    }
}

def blob_upload_conf_callback(result, user_context):
    if str(result) == 'OK':
        print ( "...file uploaded successfully." )
    else:
        print ( "...file upload callback returned: " + str(result) )

def iothub_file_upload_sample_run():
    try:
        print ( "IoT Hub file upload sample, press Ctrl-C to exit" )

        client = IoTHubClient(CONNECTION_STRING, PROTOCOL)

        #f = open(PATHTOFILE, "r")
        #content = f.read()

        #client.upload_blob_async(FILENAME, content, len(content), blob_upload_conf_callback, 0)
        client.upload_blob_async("test", data, len(content), blob_upload_conf_callback, 0)
        print ( "" )
        print ( "File upload initiated..." )

        while True:
            time.sleep(100)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
    except:
        print ( "generic error" )

if __name__ == '__main__':
    print ( "Simulating a file upload using the Azure IoT Hub Device SDK for Python" )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_file_upload_sample_run()
