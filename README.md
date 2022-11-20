# Device

## CCTV

**This code requires a Raspberry Pi and a camera sensor.**

**Check whether the camera sensor opens normally and implement it.**

In the image_send.py code, only the url path that you want to send the image data is written down and executed, and it is periodically posted.

## fire detector  
1. install firedetect.py on raspberry pi and firedetect.ino on arduino  
2. connect them with usb-b cable and command 'ls /dev/TTY' to find where arduino connected to raspberry pi  
3. change serial number and write uri of Mobius platform where you want to upload data

## fireextinguisher_alarm
1. install the file and turn it on.

## DisasterRobot
### send_data_visual, send_data_pose(Zed2 camera must be running.) 

1. Send image file for Visual Localization (send_data_visual).py)  

+ Write down the IP, port, and container URL of the Mobius server to be used. Also, write down the remote_server IP and local_IP, which will be applied to the sftp protocol for image transmission, and the directory information to which the image file belongs (in this case, the server that performs visual localization should continue to be in-ferencing). 

+ send_data_visual.When py is executed, the image is sent to the directory of the visual localization server.  

2. Extracting human joint data for pose estimation (send_data_pose.py)  

+ Write down the container URL of the Mobius server you want to use  

+ After executing send_data_pose.py, human joint data is extracted based on the image captured by the Zed2 camera and transmitted to the Mobius server.  

