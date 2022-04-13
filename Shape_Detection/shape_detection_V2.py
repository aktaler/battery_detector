# Key "q" will break camera loop
'''
TODO
Check for intersection between gripper perimeter and other rectangular boxes, maybe use contour hierarchy to just check the first one

'''
# import the necessary packages
from shapedetector import ShapeDetector
import imutils
import cv2
import numpy as np
from datetime import datetime

# switch variable for image or video stream
use_image = False

# start video
if not use_image:
    cap = cv2.VideoCapture(1)

while True:
    # start timer to estimate code execution time
    startTime = datetime.now()
    # load image from file or video stream
    if use_image:

        image = cv2.imread("battery1.jpg")

    else:

        # load the image or video feed
        ret, image = cap.read()
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame")
            continue

    # Image preprocessing gray->blurr->thresh->invert bitwise
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 2)

    # Sobel Edge Detection
    # sobelxy = cv2.Sobel(src=blurred, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)  # Combined X and Y Sobel Edge Detection
    # Canny Edge Detection
    # canny = cv2.Canny(blurred, 10, 120)

    thresh = cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY)[1]
    inverted = cv2.bitwise_not(thresh)

    # show interim images
    # cv2.imshow("soblexy", sobelxy)
    # cv2.imshow("Canny", canny)
    # cv2.imshow("thresh", thresh)
    # cv2.imshow("blurred", blurred)
    # cv2.imshow("inverted", inverted)

    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(image=inverted.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:

        # Skip over small and to large contours
        if 3000 > cv2.contourArea(c) < 25000:
            continue
        ''' not needed for now
        # compute the center of the contour
        M = cv2.moments(c)
        # Check if m00 has zero value and continue loop
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            continue
        '''

        # calculate and draw oriented rectangular box
        # we use variable rect later to draw a gripper perimeter
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (0, 0, 255), 2)

        # Retrieve the key parameters of the rotated bounding box
        center = (int(rect[0][0]), int(rect[0][1]))
        width = int(rect[1][0])
        height = int(rect[1][1])
        angle = int(rect[2])

        #swap height and width and draw gripper perimeter
        if width > height:
            rotated_box = (rect[0], (50, 120), rect[2])
        else:
            rotated_box = (rect[0], (120, 50), rect[2])

        rotated_box = cv2.boxPoints(rotated_box)
        rotated_box = np.int0(rotated_box)
        cv2.drawContours(image, [rotated_box], 0, (127, 255, 0), 3)


        #transform angle to +-90 degree system
        if width < height:
            angle = 90 - angle
        else:
           angle = -angle

        # cv2.drawContours(image, gripper_peri, 0.5, (0, 255, 0), 2)
        # run shape classification on rectangular box
        shape = sd.detect(box)

        # draw everything on the image
        # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        string_list = ["Type" + shape, "CenterX=" + str(box[0][0]), "CenterY=" + str(box[0][1]), "alpha=" + str(angle)]
        y_Offset = box[0][1]
        for i in string_list:
            cv2.putText(image, i, (box[0][0], y_Offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            y_Offset += 20

        # show the output image
        cv2.imshow("Image", image)
        # cv2.waitKey(0)

        print(datetime.now() - startTime)

    if cv2.waitKey(1) == ord('q'):
        break

# release video stream
cap.release()
cv2.destroyAllWindows()
