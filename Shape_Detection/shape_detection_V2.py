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

    # convert the image to grayscale, blur it slightly,
    # threshold it and invert
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 2)
    thresh = cv2.threshold(blurred, 110, 255, cv2.THRESH_BINARY)[1]
    inverted = cv2.bitwise_not(thresh)

    # show interim images
    cv2.imshow("thresh", thresh)
    # cv2.imshow("blurred", blurred)
    cv2.imshow("inverted", inverted)

    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(image=inverted.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:

        # Skip to small contours
        if cv2.contourArea(c) < 2000:
            continue

        # compute the center of the contour
        M = cv2.moments(c)
        # Check if m00 has zero value and continue loop
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            continue

        # calculate and draw oriented rectangular box
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (0, 0, 255), 2)

        # run shape classification on rectangular box
        shape = sd.detect(box)


        # draw everything on the image
        # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        string_list = ["Type"+shape, "CenterX="+str(cX), "CenterY="+str(cY), "alpha="+str(round(rect[2],2))]
        y_Offset = cY
        for i in string_list:
            cv2.putText(image, i, (cX, y_Offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
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
