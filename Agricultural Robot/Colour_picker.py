import cv2
import numpy as np

def empty(a):
    pass

# Creating Trackbar for colour detection
cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",640,240)

# Setting HUE, SATURATION, VALUE min and max values
cv2.createTrackbar("Hue Min","Trackbar", 10, 179, empty)
cv2.createTrackbar("Hue Max","Trackbar", 38, 179, empty)
cv2.createTrackbar("Sat Min","Trackbar", 83, 255, empty)
cv2.createTrackbar("Sat Max","Trackbar", 255, 255, empty)
cv2.createTrackbar("Val Min","Trackbar", 74, 255, empty)
cv2.createTrackbar("Val Max","Trackbar", 255, 255, empty)

while True:
    # Reading image and converting BGR to HSV image
    img = cv2.imread("C:\\Python test files\\car.jpg")
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)  

    # Getting Trackbar control
    h_min = cv2.getTrackbarPos("Hue Min","Trackbar")
    h_max = cv2.getTrackbarPos("Hue Max","Trackbar")
    s_min = cv2.getTrackbarPos("Sat Min","Trackbar")
    s_max = cv2.getTrackbarPos("Sat Max","Trackbar")
    v_min = cv2.getTrackbarPos("Val Min","Trackbar")
    v_max = cv2.getTrackbarPos("Val Max","Trackbar")
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imghsv, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    # Showing image
    cv2.imshow("Original",img)
    cv2.resizeWindow("Original",500,500)
    cv2.imshow("HSV",imghsv)
    cv2.resizeWindow("HSV",500,500)
    cv2.imshow("mask",mask)
    cv2.resizeWindow("mask",500,500)
    cv2.imshow("imgResult",imgResult)
    cv2.resizeWindow("imgResult",500,500)
    cv2.waitKey(1)

