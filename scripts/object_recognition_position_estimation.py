#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO
import numpy as np
from sensor_msgs.msg import Image, CompressedImage, CameraInfo

class ImageReceiver(object):
    def __init__(self):
        self.br = CvBridge()
        self.sub_image = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback_recognition)
        self.sub_info = rospy.Subscriber("/usb_cam/camera_info", CameraInfo, self.callback_camera_info)
        self.model = YOLO("yolov8n.pt")

    def callback_camera_info(self, data):
        print(data)
        # obtain K matrix from a K vector
        k_vector = data.K
        self.k_matrix = np.reshape((k_vector), (-1,3))
        print(self.k_matrix)
        self.sub_info.unregister()

    def callback_recognition(self, msg):
        rospy.loginfo('Image received...')
        self.image = self.br.imgmsg_to_cv2(msg)
        img = self.image

        prediction = self.model.predict(img, save=False, save_txt=False)

        try:
            # Take class id
            #class_id = prediction[0].boxes[0].cls[0].item()
            # Take string from list of objects through class id
            #print(prediction[0].boxes[0].xyxy[0])
            #print("Predicted object:", prediction[0].names[class_id])

            #emulated distances & recognition
            x_center = 100
            y_center = 300
            floor_distance = 5

            #3D point calculation
            [X,Y,Z] = (np.dot(np.linalg.pinv(self.k_matrix), np.array([x_center*floor_distance, y_center*floor_distance, floor_distance])))
            print([X,Y,Z])

        except (AttributeError, IndexError):
            print("Prediction Error YOLO")

def main():
    print("Position Estimation in ROS")
    sub = ImageReceiver()
    # Initialize the subscriber node
    rospy.init_node('listener', anonymous=True)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
