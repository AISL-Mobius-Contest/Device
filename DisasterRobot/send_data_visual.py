#!/usr/bin/python3
from matplotlib import container
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
import socket
from _thread import *
import time
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
import json
import requests
from requests.exceptions import HTTPError
from kafka import KafkaConsumer, KafkaProducer
import cv2
import numpy as np
import time

import base64

import requests

import time
import pysftp

import json

# import pysftp
host = 'your host IP'
# host = 'your inference server IP'

port = 'port'
# port = 'your ssh or scp or sctp port'

username = 'username'
# username = 'username'

password = 'password'
# password = 'password'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


local_path = 'local_path'

remote_path = 'remote_path'
# remote_path = 'your inference server image root dir'

class SendData2(Node):
    def __init__(self):
        super().__init__('ZedSub')
        qos_profile = QoSProfile(depth=10)


        self.url = "http://Your_Mobius_Server/Cam_Container"

        self.headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'Cam_Container',
        'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
        }


        self.image_data = []
        self.reshaped_img=[]
        self.subnode = self.create_subscription(
        Image,
        '/zed2/zed_node/right/image_rect_color',
        self.image_callback,
        qos_profile)
        self.cnt = 0

    def rgba2rgb(self, rgba, background=(255,255,255) ):
        row, col, ch = rgba.shape
        if ch == 3:
            return rgba

        assert ch == 4, 'RGBA image has 4 channels.'

        rgb = np.zeros( (row, col, 3), dtype='float32' )

        rgb[:,:,0] = rgba[:,:,0]
        rgb[:,:,1] = rgba[:,:,1]
        rgb[:,:,2] = rgba[:,:,2]

        return np.asarray( rgb, dtype='uint8' )


    def image_callback(self, msg):

        self.image_data = np.array(msg.data.tolist())
        print(self.cnt)
        self.cnt += 1
        self.reshaped_img = np.array(np.reshape(self.image_data, (720, 1280, 4)), dtype=np.float32)
        rgb_data = self.rgba2rgb(self.reshaped_img)


        
        # FOR QUERY
        file_name = 'query.jpg'
        cv2.imwrite('./query.jpg', rgb_data)

        
        # FOR QUERY
        time.sleep(2)
        


        ####sftp######################
        with pysftp.Connection(host, port=port, username=username, password=password, cnopts=cnopts) as sftp:           
            sftp.put(local_path+file_name, remote_path+'/'+file_name)

            sftp.close()

        data = [{'img_path': remote_path}]
        data = json.dumps(data)
        payload = "{\n    \"m2m:cin\": {\n        \"con\": "+ data +"}\n}"
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        print(response.text)


def main(args=None):
    rclpy.init(args=args)
    node = SendData2()

    try:
        print('init')
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt")
        sftp.close()
        transprot.close()
    
    finally:
        node.destroy_node()
        rclpy.shutdown()
    

if __name__ == "__main__":
    main()


