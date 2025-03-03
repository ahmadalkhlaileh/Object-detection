# Object-detection

# Key Steps:

Open the video file and initialize the necessary objects.
Read the first two frames for motion analysis.
Process the frames by:
Computing the absolute difference between frames.
Converting the difference to grayscale.
Applying Gaussian blur to reduce noise.
Using thresholding to create a binary mask.
Dilating the binary mask to fill gaps.
Detecting moving objects using contours.
Drawing rectangles around detected objects.
Save the processed frame to an output video.
Display the processed video, allowing the user to exit with Esc.
