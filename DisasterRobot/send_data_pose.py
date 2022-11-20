from matplotlib import container
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
import socket
from _thread import *
import time
from std_msgs.msg import Bool
from zed_interfaces.msg import ObjectsStamped
import json
import requests
from requests.exceptions import HTTPError
# from post import posting

def posting(data):
    url = "http://Your_Mobius_Server/joint_container"

    payload = "{\n    \"m2m:cin\": {\n        \"con\": "+ data +"}\n}"

    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'Joint_container',
    'Content-Type': 'application/json; ty=4'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


class SendData(Node):
    def __init__(self):
        super().__init__('ZedSub')
        qos_profile = QoSProfile(depth=10)
        self.linear_x = 0.0
        self.linear_y = 0.0
        self.linear_z = 0.0

        self.angular_x = 0.0
        self.angular_y = 0.0
        self.angular_z = 0.0

        self.objects = []
        
        self.label_id = 0
        self.skeleton_available = list()
        self.bounding_box = list([0] * 3 for _ in range(8))
        self.bounding_box_head = list([0] * 3 for _ in range(8))
        self.skeleton = list([0] * 3 for _ in range(34))
        self.skeleton_head = [0, 0, 0]
        self.position = [0, 0, 0]

        
        self.subnode = self.create_subscription(
            ObjectsStamped,
            'zed2/zed_node/obj_det/objects',
            self.human_callback,
            qos_profile
        )


    def human_callback(self, msg):
        self.objects = msg.objects
        #self.skeleton_available = self.objects[]

        if self.objects == []:
            pass
            self.get_logger().info('-------------------------------------------')
            self.get_logger().info('Not Found Person')
            self.get_logger().info('-------------------------------------------')
            
        #print(msg.objects)

        else:
            #self.label_id = msg.objects[0].label_id
            
            bbox_list = list()
            bbox_head_list = list()
            skeleton_list = list()
            self.position = list()
            skeleton_head_list = list()
            for k in range(len(self.objects)):
                for i in range(len(self.bounding_box)):
                    for j in range(len(self.bounding_box[i])):
                        self.bounding_box[i][j] = msg.objects[k].bounding_box_3d.corners[i].kp[j]
                    #print(self.bounding_box)
                        self.bounding_box_head[i][j] = msg.objects[k].head_bounding_box_3d.corners[i].kp[j]
                    #print(self.bounding_box_head)
                bbox_list.append(self.bounding_box)
                self.bounding_box = list([0] * 3 for _ in range(8))
                bbox_head_list.append(self.bounding_box_head)
                self.skeleton_available.append(self.objects[k].skeleton_available)

                    
            for k in range(len(self.objects)):
                for i in range(len(self.skeleton)):
                    for j in range(len(self.skeleton[i])):
                        self.skeleton[i][j] = msg.objects[k].skeleton_3d.keypoints[i].kp[j]
                skeleton_list.append(self.skeleton)
                self.skeleton = list([0] * 3 for _ in range(34))
                self.skeleton_head = msg.objects[k].head_position
                self.position.append(list(msg.objects[k].position))

            obj_list = []
            for i in range(len(self.objects)):
                obj_list.append({"label_id": str(self.objects[i].label_id),"bounding_box": str(bbox_list[i]),"bounding_box_head": str(bbox_head_list[i]),"skeleton": str(skeleton_list[i]),
                "skeleton_head": str(list(self.objects[i].head_position)),"position" : str(self.position[i])})
                
                data = {"result":obj_list,"source":"Mobius/Container"}

                obj_str = json.dumps((data))

                print(obj_str)

                posting(obj_str)



def main(args=None):
    rclpy.init(args=args)
    node = SendData()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt")

    
    finally:
        node.destroy_node()
        rclpy.shutdown()
    

if __name__ == "__main__":
    main()



