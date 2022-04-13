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
        if 3500 < area < 5000:
            shape = "AAAA"

        elif 6000 < area < 7500:
            shape = "AAA"

        elif 8000 < area < 9000:
            shape = "AA"

        elif 15000 < area < 20000:
            shape = "9V"

        # print(shape, str(area))
        # return the name of the shape
        return shape