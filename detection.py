import cv2
import numpy as np

# Open the video file for capture
cap = cv2.VideoCapture('tracking_3.avi')

# Get the frame width and height of the video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID') #*'XVID': This syntax is used in Python to pass individual characters of the string 'XVID' as separate arguments to the function. Essentially, it unpacks the string into individual characters
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (frame_width, frame_height))

# Read the first two frames
ret, frame1 = cap.read()  # 1st frame
ret, frame2 = cap.read()  # 2nd frame

# Loop through the video frames
while cap.isOpened():
    # Check if the frame was successfully read
    if not ret:
        break

    # Compute the absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)
    
    # Convert the difference image to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding to create a binary image
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    # Dilate the thresholded image to fill gaps
    dilated = cv2.dilate(thresh, None, iterations=3)
    
    # Find contours of objects in the dilated image
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over each contour
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # If the contour area is less than 900 pixels, skip
        if cv2.contourArea(contour) < 900:
            continue

        # Draw a rectangle around the detected object
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # (Optional) Put text on the frame to indicate movement status
        # cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Resize the frame to original size and write it to the output video
    image = cv2.resize(frame1, (frame_width, frame_height))
    out.write(image)
    
    # Display the frame with detected motion
    cv2.imshow("feed", frame1)
    
    # Update frame1 and frame2 for the next iteration
    frame1 = frame2
    ret, frame2 = cap.read()  # Read the next frame
    
    # Check for 'Esc' key press to break the loop
    if cv2.waitKey(40) == 27:
        break

# Release the video capture, video writer, and close OpenCV windows
cv2.destroyAllWindows()
cap.release()
out.release()
