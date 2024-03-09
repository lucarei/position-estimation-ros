# position-estimation-ros
Low Cost Approach for Robotic Position Estimation in ROS Noetic

First of all you need to install usb_cam package to have a webcam ROS compliant.

1. command for list of connected webcams 'ls -l /dev/video*'
2. modify the launch script for usb_cam to add your webcam.
>/opt/ros/noetic/share/usb_cam/launch, then create your own launch file with the right video stream.
3. test it using the roslaunch command: now the stream is inside the ROS environment, even inside RVIZ.