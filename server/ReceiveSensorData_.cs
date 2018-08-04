using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Runtime.Serialization;
using System.Xml;
using UnityEngine;

namespace MotorBoat
{
    public class ReceiveSensorData
    {
        int LOCALPORT = 5000;
        Thread receiveThread;
        bool messageReceived = false;
        Queue<float> queue;

        public ReceiveSensorData(Queue<float> queue)
        {
            this.queue = queue;
        }

        public void StartReceive()
        {
            receiveThread = new Thread(new ThreadStart(Receive));
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }

        public void StopReceive()
        {
            if (receiveThread != null)
            {
                receiveThread.Abort();
                receiveThread.Join();
                receiveThread = null;
            }
        }

        UdpClient OpenPort()
        {
            UdpClient udpClient;
            try
            {
                udpClient = new UdpClient(LOCALPORT);
                Debug.Log("UDP port was set.");
                return udpClient;
            }
            catch (Exception e)
            {
                Debug.Log("Error: " + e.Message);
                StartReceive();
                return new UdpClient();
            }
        }

        void Receive()
        {
            UdpClient udpClient = OpenPort();
            IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, LOCALPORT);
            UdpState state = new UdpState(remoteEP, udpClient);
            while (true)
            {
                udpClient.BeginReceive(new AsyncCallback(ReceiveCallback), state);
                while (!messageReceived)
                {
                    Thread.Sleep(100);
                }
                messageReceived = false;
            }
        }

        void ReceiveCallback(IAsyncResult ar)
        {
            UdpClient udpClient = ((UdpState)(ar.AsyncState)).udpClient;
            IPEndPoint remoteEP = ((UdpState)(ar.AsyncState)).remoteEP;

            Byte[] receiveBytes = udpClient.EndReceive(ar, ref remoteEP);
            string receiveJson = System.Text.Encoding.ASCII.GetString(receiveBytes);
            var receiveData = JsonUtility.FromJson<SensorData>(receiveJson);
            Debug.Log("TimeStamp: " + receiveData.timeStamp + ", longtitude: " + receiveData.position.latitude.ToString());
            queue.Enqueue(receiveData.position.latitude);
            queue.Enqueue(receiveData.position.longitude);
            queue.Enqueue(receiveData.angular.x);
            queue.Enqueue(receiveData.angular.y);
            queue.Enqueue(receiveData.angular.z);
            //queue.Enqueue(receiveData.direction.x);
            //queue.Enqueue(receiveData.direction.y);
            //queue.Enqueue(receiveData.direction.z);
            messageReceived = true;
        }
    }

    public class UdpState
    {
        public IPEndPoint remoteEP;
        public UdpClient udpClient;

        public UdpState(IPEndPoint remoteEP, UdpClient udpClient){
            this.remoteEP = remoteEP;
            this.udpClient = udpClient;
        }
    }

    [Serializable]
    public class SensorData{
        public Position position;
        public ThreeAxis accelarate;
        public ThreeAxis angular;
        public ThreeAxis direction;
        public int boatNumber;
        public string timeStamp;
    }

    [Serializable]
    public class ThreeAxis
    {
        public float x;
        public float y;
        public float z;
    }
    [Serializable]
    public class Position{
        public float longitude;
        public float latitude;
    }
}
