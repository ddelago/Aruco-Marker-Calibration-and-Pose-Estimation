import numpy
import cv2
from cv2 import aruco
import argparse
import pickle
import glob
import os

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to the calibration video")
ap.add_argument("-c", "--captures", required=True,
	help="minimum number of valid captures required", type=int)
args = vars(ap.parse_args())

# ChAruco board variables
CHARUCOBOARD_ROWCOUNT = 7
CHARUCOBOARD_COLCOUNT = 5 
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_5X5_50)

# Create constants to be passed into OpenCV and Aruco methods
CHARUCO_BOARD = aruco.CharucoBoard_create(
	squaresX=CHARUCOBOARD_COLCOUNT,
	squaresY=CHARUCOBOARD_ROWCOUNT,
	squareLength=0.04,
	markerLength=0.02,
	dictionary=ARUCO_DICT)

# Corners discovered in all images processed
corners_all = []

# Aruco ids corresponding to corners discovered 
ids_all = [] 

# Determined at runtime
image_size = None 

# This requires a video taken with the camera you want to calibrate
cap = cv2.VideoCapture(args["video"])

# The more valid captures, the better the calibration
validCaptures = 0

# Loop through frames
while cap.isOpened():

	# Get frame
	ret, img = cap.read()

	# If camera error, break
	if ret is False:
		break

	# Grayscale the image
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Find aruco markers in the query image
	corners, ids, _ = aruco.detectMarkers(
		image=gray,
		dictionary=ARUCO_DICT)
	
	# If none found, take another capture
	if ids is None:
		continue

	# Outline the aruco markers found in our query image
	img = aruco.drawDetectedMarkers(
		image=img, 
		corners=corners)

	# Get charuco corners and ids from detected aruco markers
	response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
		markerCorners=corners,
		markerIds=ids,
		image=gray,
		board=CHARUCO_BOARD)

	# If a Charuco board was found, collect image/corner points
	# Requires at least 20 squares for a valid calibration image
	if response > 20:
		# Add these corners and ids to our calibration arrays
		corners_all.append(charuco_corners)
		ids_all.append(charuco_ids)
		
		# Draw the Charuco board we've detected to show our calibrator the board was properly detected
		img = aruco.drawDetectedCornersCharuco(
			image=img,
			charucoCorners=charuco_corners,
			charucoIds=charuco_ids)
	
		# If our image size is unknown, set it now
		if not image_size:
			image_size = gray.shape[::-1]
		
		# Reproportion the image, maxing width or height at 1000
		proportion = max(img.shape) / 1000.0
		img = cv2.resize(img, (int(img.shape[1]/proportion), int(img.shape[0]/proportion)))

		# Pause to display each image, waiting for key press
		cv2.imshow('Charuco board', img)
		if cv2.waitKey(0) == ord('q'):
			break

		validCaptures += 1
		if validCaptures == args["captures"]:
			break

# Destroy any open CV windows
cv2.destroyAllWindows()

# Show number of valid captures
print("{} valid captures".format(validCaptures))

if validCaptures < args["captures"]:
	print("Calibration was unsuccessful. We couldn't detect enough charucoboards in the video.")
	print("Perform a better capture or reduce the minimum number of valid captures required.")
	exit()

# Make sure we were able to calibrate on at least one charucoboard
if len(corners_all) == 0:
	print("Calibration was unsuccessful. We couldn't detect charucoboards in the video.")
	print("Make sure that the calibration pattern is the same as the one we are looking for (ARUCO_DICT).")
	exit()
print("Generating calibration...")

# Now that we've seen all of our images, perform the camera calibration
calibration, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
	charucoCorners=corners_all,
	charucoIds=ids_all,
	board=CHARUCO_BOARD,
	imageSize=image_size,
	cameraMatrix=None,
	distCoeffs=None)
		
# Print matrix and distortion coefficient to the console
print("Camera intrinsic parameters matrix:\n{}".format(cameraMatrix))
print("\nCamera distortion coefficients:\n{}".format(distCoeffs))
		
# Save the calibrationq
f = open('./CameraCalibration.pckl', 'wb')
pickle.dump((cameraMatrix, distCoeffs, rvecs, tvecs), f)
f.close()
		
# Print to console our success
print('Calibration successful. Calibration file created: {}'.format('CameraCalibration.pckl'))