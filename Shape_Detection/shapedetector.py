# import the necessary packages
import cv2
class ShapeDetector:

    def __init__(self):
        pass

    def detect(self, c):

        # initialize the shape name and calculate area of given contour
        shape = "unidentified"
        area = cv2.contourArea(c)

        #compare Area to couple of values
        if 2000 < area < 3000:
            shape = "AAAA"

        elif 3000 < area < 4500:
            shape = "AAA"

        elif 6000 < area < 7500:
            shape = "AA"

        elif 12000 < area < 15000:
            shape = "9V"

       # return the name of the shape
        return shape