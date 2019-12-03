# Aruco Marker Calibration and Pose Estimation
This repository shows how to generate aruco boards, calibrate a camera using those boards, and live pose estimation on those boards.

### Installing
1. Project was built using a VM running Ubuntu 18.04
2. Install opencv-contrib.
    - `pip install opencv-contrib-python`
3. `git clone https://github.com/ddelago/Aruco-Marker-Calibration-and-Pose-Estimation.git`
4. Other various packages as well, just `pip install` them as you encounter them. 

### Generating ArUco Calibration Markers
There are three ways to generate calibration markers. 
1. Single Marker
    - Generate a single ArUco marker. Can choose specific marker ID and image size.
    - `python generate_aruco.py`
2. ArUco Grid
    - Generates a grid of ArUco markers. 
    - `python generate_arucoGrid.py`
3. ChArUco Grid
    - Generates a chessboard filled with ArUco markers. This is the ideal method to use when calibrating.
    - `python generate_ChAruco.py`  

### Calibration
In orer to track objects correctly, you need to use a calibration using the camera that you will use! The calibration files in this repository were created using a Logitech C920 camera.
![alt text](https://github.com/ddelago/Aruco-Marker-Calibration-and-Pose-Estimation/blob/master/doc/ChArucoCalib.PNG)
1. Record a video of your ChAruco board in various positions. A 10-20 second long video will work. 
2. Use the `calibration_ChAruco.py` program to calibrate your camera. You need to specify where your calibration video is as well as the minimum number of valid ChAruco board captures you want. At least 40 valid captures worked for me. 
    `python calibration_ChAruco.py -v calibration_video.webm -c 80`

### Marker Tracking
After calibration, the tracking of each marker can now be performed.
- Use `python pose_marker.py` to draw an axis on each Aruco marker found.
- Use `python pose_marker.py cube` to draw a cube instead.
![alt text](https://github.com/ddelago/Aruco-Marker-Calibration-and-Pose-Estimation/blob/master/doc/PoseEstimation.gif)
