import socket
import csv
import json
from datetime import datetime
import base64

host = socket.gethostbyname(socket.gethostname())
port =  5000
bufsize = 4096

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(0.01)
sock.bind((host,port))
sock.setblocking(0)

data =''
address = ''

#filename = os.rename("sample.txt", "{0:%Y%m%d_%H%M%S}.txt".format(d))
now = datetime.now()
#現在時刻を織り込んだファイル名を生成
file_name = "sensordata_{0:%Y%m%d-%H%M%S}.csv".format(now)

def support_datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")

print('wait at：{0}'.format(host))

with open(file_name, 'w', newline='') as csvFile:
	csvwriter = csv.writer(csvFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	csvwriter.writerow(['t', 'boat', '緯度', '経度', 'accelx','accely','accelz','傾きx','傾きy','傾きz','方角x','方角y','方角z'])

	while True:
		try:
			data,address = sock.recvfrom(bufsize)
		except socket.error:
			pass
		else:
			print ("from:", address)
			print ("recvd:", data)
			csv_ = json.loads(data.decode("UTF-8"))
			time = csv_["timeStamp"]
			boat = csv_["boatNumber"]
			position =  json.loads(json.dumps(csv_["position"]))
			longitude = position["longitude"]
			latitude = position["latitude"]
			accel =json.loads(json.dumps(csv_["accelaration"]))
			accelx = accel["x"]
			accely = accel["y"]
			accelz = accel["z"]
			tilt = json.loads(json.dumps(csv_["angular"]))
			tiltx = tilt["x"]
			tilty = tilt["y"]
			tiltz = tilt["z"]
			direction = json.loads(json.dumps(csv_["direction"]))
			directx = direction["x"]
			directy = direction["y"]
			directz = direction["z"]

			csvwriter.writerow([time,boat,longitude,latitude,accelx,accely,accelz,tiltx,tilty,tiltz,directx,directy,directz])				
        #s.sendto("recvd:" + data, address)

