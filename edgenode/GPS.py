# coding: UTF-8
import serial
import sys,os
import threading
import time

sys.path.append('/home/nodens/micropyGPS')

import micropyGPS

gps = micropyGPS.MicropyGPS(9, 'dd') 
# MicroGPSオブジェクトを生成する。
# 引数はタイムゾーンの時差と出力フォーマット

def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s = serial.Serial('/dev/serial0', 9600, timeout=10)
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)


def getGPS():
    #if gps.clean_sentences > 20:
    #ちゃんとしたデーターがある程度たまったら出力する
    #gps time stamp
    #h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
    return(gps.latitude[0],gps.longitude[0],gps.altitude) 

        #print(gps.satellites_used) 
        #print('衛星番号: (仰角, 方位角, SN比)')
        #for k, v in gps.satellite_data.items():
        #    print('%d: %s' % (k, v))
        #print('')
