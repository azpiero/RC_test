import socket
#from contextlib import closing
import sys
import json
from contextlib import closing
from datetime import datetime
import time

#s = socket.socket()
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



host = "192.168.100.100"
port = 5000

#with closing(s):
#s.connect((host, port))
#s.send(json.dumps(data))
with closing(client):
    for i in range(10):
        json_string ={
            "timeStamp" : datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "boatNumber": "3",
            "position": {
                "longitude": "135.1",
                "latitude": 30 + i
                },
            "accelaration": {
                "x ": "100",
                "y": "200",
                "z": "300"
                },
            "angular": {
                "x": "1",
                "y": "2",
                "z": "3"
                },
            "direction": {
                "x": "10.1",
                "y": "20.2",
                "z": "30.3"
                }
            }
        client.sendto(str.encode(json.dumps(json_string)),("192.168.100.100",5000))
        i +=1
        time.sleep(1)



#data,addr = client.recvfrom(4096) #レシーブは適当な2の累乗にします（大きすぎるとダメ）
