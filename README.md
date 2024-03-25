# position-estimation-ros
### Low-Cost Approach for Robotic Position Estimation in ROS Noetic

## Camera Calibration

1. Download and print your preferred [chessboard](https://markhedleyjones.com/projects/calibration-checkerboard-collection).

> NOTE: you need know number of internal rows/columns and checker size.

2. take at least 30 images at different angles using different angles (pressing 's' button, 'q' to quit)

3. run calibration script.

The calibration can be done with a ROS compliant tool.

>rosrun camera_calibration cameracalibrator.py --size 7x4 --square 0.35 image:=/usb_cam/image_raw/

The GUI will show you the chessboard architecture with points and colors. It automatically saves images increasing different parameters: skew, size, x, y. When the software recognize a lot of different images (40 in my case), you are able to calibrate the camera and obtain the different matrices. Ther are saved as 'tar.gz' file in /tmp/ folder.

> ost.yaml file is in the calibrationdata.tar.gz file saved during the calibraton process

To extract the file:

> tar -xvzf calibrationdata.tar.gz -C /home/luca/Desktop/

save it as head_camera into hidden '.ros/camera_info/' folder

> mv head_camera.yaml /home/luca/.ros/camera_info/

to test the calibrated camera info on ROS topics, launch the usb_cam package, then:

> rostopic echo /usb_cam/camera_info

## Test Camera Calibration [ON HOLD]

THIS PART IS ON HOLD SINCE IT WILL BE USE ONLY TO VERIFY CALIBRATION MATRIX.

>sudo apt install ros-noetic-aruco-ros

install aruco_ros package, then add the correct topic of your camera in the launch file.

>         <remap from="/camera_info" to="/usb_cam/camera_info" />  <remap from="/image" to="/usb_cam/image_raw" />

## USB Camera Images in ROS Environment

First of all, you need to install the `usb_cam` package to have a ROS-compliant webcam (which publishes images in the ROS infrastructure).

1. To list connected webcams, use the command: `ls -l /dev/video*`.
2. Modify the launch script for `usb_cam` to add your webcam (please download this launch file from the ROS repositories, as it is not reported here).
   - The launch file is located at `/opt/ros/noetic/share/usb_cam/launch`. Create your own launch file with the appropriate video stream.
3. Test it using the `roslaunch` command: now the stream is available within the ROS environment, including RVIZ.
   - Example: `roslaunch usb_cam usb_test_pe.launch`
4. While the camera is capturing data, you can run the basic script for object recognition (`object_recognition_yolo_ros`). You can use it as a skeleton for your own AI and computer vision applications.
   - **Note 1**: You need to install several libraries (e.g., `ultralytics`) using the Python package manager (PIP).

## Position Estimation [UNDER DEVELOPMENT]

Run camera using ROS launch file for usb_camera.

> be sure to publish camera info under /usb_camera/camera_info/ topic

Run 'object_recognition_position_estimation' script. For now it will give a fixed and fake 3D position.

### Rosserial [FUTURE DEVELOPMENT for SENSOR CONTROL]

rosserial temp workaround
ros/msg.h file #include <cstring> no longer works, replace it with #include <string.h> and the std::memcpy() function is not a part of std anymore, so change it to memcpy().


rosserial library for arduino
roscore
Next, run the rosserial client application that forwards your Arduino messages to the rest of ROS. Make sure to use the correct serial port:
rosrun rosserial_python serial_node.py /dev/ttyUSB0

install all the rosserial dependancies (base, arduino, python)