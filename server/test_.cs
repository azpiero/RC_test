using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MotorBoat;
using System;

public class test : MonoBehaviour {
    ReceiveSensorData receiveSensorData;
    Queue<float> queue;


	void Start () {
        Debug.Log("start");
        queue = new Queue<float>();
        receiveSensorData = new ReceiveSensorData(queue);
        //        receiveSensorData.StartReceive();
        receiveSensorData.StartReceive();
	}
    void Update()
    {
        if(queue.Count != 5S ){
            transform.position = new Vector3(queue.Dequeue() - 2.004095f, 7.13982f, queue.Dequeue() - 30.0f);
            transform.Rotate(new vector3(queue.Dequeue(),queue.Dequeue(),queue.Dequeue()))
        }
    }

    void OnDestroy()
    {
        if (receiveSensorData != null){
            receiveSensorData.StopReceive();
        }
    }
}
