#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO

class ImageReceiver(object):
    def __init__(self):
        self.br = CvBridge()
        self.sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
        self.model = YOLO("yolov8n.pt")

    def callback(self, msg):
        rospy.loginfo('Image received...')
        self.image = self.br.imgmsg_to_cv2(msg)
        img = self.image

        prediction = self.model.predict(img, save=False, save_txt=False)

        try:
            # Take class id
            class_id = prediction[0].boxes[0].cls[0].item()
            # Take string from list of objects through class id
            print("Predicted object:", prediction[0].names[class_id])

        except (AttributeError, IndexError):
            print("Prediction Error YOLO")

def main():
    # Create an instance of the subscriber
    sub = ImageReceiver()
    # Initialize the subscriber node
    rospy.init_node('listener', anonymous=True)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
