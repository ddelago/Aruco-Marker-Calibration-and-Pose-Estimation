# AR-Projection-Mapping
This repository contains two implementations of AR Projection Mapping. In particular, it includes the calibration of the projector-camera pair using [ArUco](https://docs.opencv.org/3.1.0/d9/d6d/tutorial_table_of_content_aruco.html) markers and the implementation of two versions of projection *tracking*. **View presentation of this work [here](https://docs.google.com/presentation/d/1bUq5LVSlZjvOn33RQa834XeI6kKK9QSm9t-LNzdupIU/edit?usp=sharing) to get a high level overview.**

### Installing
1. Project was built using a VM running Ubuntu 18.04
2. Install opencv-contrib.
    - `pip install opencv-contrib-python`
2. `git clone https://github.com/ddelago/AR-Projection-Mapping.git`

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
![alt text](https://github.com/ddelago/AR-Projection-Mapping/blob/master/pictures/stereoCalib.PNG)
1. The first calibration method involves using images of a ChArUco board in various positions. The images are located in the `~/pictures` folder.
    - `python calibration_ChAruco.py`
2. The second calibration method is a **stereo** calibration method that uses a combination of a physical ChArUco board along with a projected circle grid. 
    - See the ChAruco_Circles.webm calibration video to view an example.
    - Based off the calibration method [here](https://www.morethantechnical.com/2017/11/17/projector-camera-calibration-the-easy-way/).
    - This method treats the projector as the second camera in a stereo camera pair in order to get the transformation from the actual camera to the projectors perspective.
    - Needs a circle grid as well as a ChArUco board. To generate, use the `~/patterns/gen_pattern.py` file. Instructions on how to use the program can be seen [here](https://docs.opencv.org/master/da/d0d/tutorial_camera_calibration_pattern.html). An already generated board can be found here: `~/patterns/test_circleGrid.png`
    - `python calibration_ChArucoWithCircles.py`

### Marker Tracking
After calibration, the tracking of each marker can now be performed.
![alt text](https://github.com/ddelago/AR-Projection-Mapping/blob/master/pictures/perspTrans.PNG)
1. **Tracking Using Stereo Calibration**
    - **_This method is not fully implemented_**
    - Will track markers correctly when viewing the stream from your camera, but will not reproject correctly from the projector.
    - `python pose_marker.py`
2. **Tracking with Perspective Transform**
    - This method uses a [perspective transform ](https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/) to correctly reproject the markers position.
    - `python pose_markerPerpTrans.py`
    - This will output 2 windows, 'Project Image' and 'Input Image'. 
    - Move the 'Project Image' (will have 4 ArUco markers) window to your projector display and fullscreen the window. 
    - This program will detect the ArUco markers in each of the corners and then correctly transform the perspective. It specifically looks for markers with ID 0, 1, 2, and 3. 
