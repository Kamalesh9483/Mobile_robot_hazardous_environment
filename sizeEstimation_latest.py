#detect irregular shape and contour area and print size
import cv2
import imutils # image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, 
import imutils.perspective as persp # order contour cordinates - left, right, top, bottom
import scipy.spatial.distance as dist # to find distance
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from numpy import asarray
#set the image path 
img_path = 'C:\Projects\Mobile robot in hazardous environment\size estimation\images'

# change the directory to image path
os.chdir(img_path)
img = cv2.imread('soil_img4.jpg') #BGR

#convert to RGB for matplot
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#show the image
plt.figure(figsize=(15,15))
#plt.imshow(rgb_img)
#plt.show()

#convert image to gray scale for detecting the contours
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#show image in gray
#rgb_img = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
#plt.imshow(rgb_img)
#plt.show()

# Creating Trackbar for colour detection
cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",640,640)

def empty(a):
    pass

# Setting HUE, SATURATION, VALUE min and max values
cv2.createTrackbar("thresh Min","Trackbar", 0, 200, empty)
cv2.createTrackbar("thresh Max","Trackbar", 0, 255, empty)
cv2.createTrackbar("kernel Min","Trackbar", 0, 50, empty)
cv2.createTrackbar("kernel Max","Trackbar", 0, 50, empty)
cv2.createTrackbar("itr_dilation","Trackbar", 0, 10, empty)
cv2.createTrackbar("itr_erosion","Trackbar", 0, 10, empty)
cv2.createTrackbar("gauss_blur","Trackbar", 0, 7, empty)
cv2.createTrackbar("canny_l","Trackbar", 0, 100, empty)
cv2.createTrackbar("canny_u","Trackbar", 0, 100, empty)


while True:
       # Getting Trackbar control
    thresh_min = cv2.getTrackbarPos("thresh Min","Trackbar")
    thresh_max = cv2.getTrackbarPos("thresh Max","Trackbar")
    kernel_min = cv2.getTrackbarPos("kernel Min","Trackbar")
    kernel_max = cv2.getTrackbarPos("kernel Max","Trackbar")
    itr_dil = cv2.getTrackbarPos("itr_dilation","Trackbar")
    itr_ero = cv2.getTrackbarPos("itr_erosion","Trackbar")
    gaussian_blur = cv2.getTrackbarPos("gauss_blur","Trackbar")
    cannyfilter_l = cv2.getTrackbarPos("canny_l","Trackbar")
    cannyfilter_u = cv2.getTrackbarPos("canny_u","Trackbar")

#remove noise using threshold
    # thresh, thresh_img = cv2.threshold(gray, thresh_min, thresh_max, cv2.THRESH_BINARY_INV) # cv2.threshold(gray, thresh value, brightness, cv2.THRESH_BINARY)
    #show image in Thresh
    # rgb_img = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2RGB)

    # lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=1)
    # lap = np.uint8(np.absolute(lap))
    # sobelX = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    # sobelY = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    # sobelX = np.uint8(np.absolute(sobelX))
    # sobelY = np.uint8(np.absolute(sobelY))
    # sobelCombined = cv2.bitwise_or(sobelX, sobelY)
    thresh, thresh_img = cv2.threshold(gray, thresh_min, thresh_max, cv2.THRESH_BINARY) # cv2.threshold(gray, thresh value, brightness, cv2.THRESH_BINARY)
    rgb_img = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2RGB)
    kernel = np.ones((kernel_min, kernel_max), np.uint8)
    img_dilation = cv2.dilate(thresh_img, kernel, iterations= itr_dil)
    img_erosion = cv2.erode(img_dilation, kernel, iterations= itr_ero)
    # imgBlur = cv2.GaussianBlur(img_erosion,(gaussian_blur, gaussian_blur),1)
    # imgCanny1 = cv2.Canny(sobelCombined, cannyfilter_l, cannyfilter_u)
   
    #show image in Thresh
    
    # kernel = np.ones((kernel_min, kernel_max), np.uint8)
    # img_dilation = cv2.dilate(rgb_img, kernel, iterations= itr_dil)
    # img_erosion = cv2.erode(img_dilation, kernel, iterations= itr_ero)
    # imgBlur = cv2.GaussianBlur(img_erosion,(gaussian_blur, gaussian_blur),1)
    # imgCanny1 = cv2.Canny(imgBlur, cannyfilter_l, cannyfilter_u)
    
    cv2.imshow("Threshed",img_erosion)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# plt.imshow(rgb_img)
# plt.show()

# find the total contours
conts = cv2.findContours(img_erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print('Total number of contours using cv2 are ', len(conts))
#fine tune contours by cv2 using imutils
conts = imutils.grab_contours(conts)
print('Total number of contours using imutils are ', len(conts))

# asarray() class is used to convert
# PIL images into NumPy arrays
numpydata = asarray(img)
  
# above array
# data = Image.fromarray(numpydata)

#create empty image with original dimension
# cont_img = np.zeros(img.shape)
cont_img = numpydata
#plt.imshow(cont_img)
#plt.show()

#draw the contours in the empty image - cont_img
cont_img = cv2.drawContours(cont_img, conts, -1, (0,255,0), 1)

# plt.imshow(cont_img)
# plt.show()

#midpoint definition
def midPoint(ptA, ptB):
    return ((ptA[0] + ptB[0])/2, (ptA[1] + ptB[1])/2)

# #loop over all the contour coordinates
for c in conts:
    # extract box points
    box = cv2.minAreaRect(c) #(left, top), (right, bottom), accuracy 
    print(box)
    box = cv2.boxPoints(box)
    #convert box points to integer
    box = np.array(box, dtype='int')
    
    if cv2.contourArea(c) < 500:
        continue
        
    #draw contour
  
    cv2.drawContours(cont_img, [c], -1, (0,255,0), 1)
    cv2.drawContours(cont_img, [box], -1, (255,255,255), 1)
    
    #print(box)
    for (x,y) in box:
        cv2.circle(cont_img, (x, y), 2, (255, 0, 0), 2)
        (tl, tr, br, bl) = box
       
        #calculate midpoints for top-bottom of rectangle
        (tlX, trX) = midPoint(tl, tr)
        (brX, blX) = midPoint(br, bl)
        
        #draw midpoint dots for top and bottom
        cv2.circle(cont_img, (int(tlX), int(trX)), 1, (255, 0, 0), 2)
        cv2.circle(cont_img, (int(brX), int(blX)), 1, (255, 0, 0), 2)
        
        #connect the midpoints using line
        cv2.line(cont_img, (int(tlX), int(trX)), (int(brX), int(blX)), (255, 255, 255), 1)
        
        #calculate the distance based on midpoints
        dA = dist.euclidean((tlX, trX), (brX, blX))
        
        #print the size in pixel in each contour rectangle
        cv2.putText(cont_img, "{:.1f} px".format(dA), (int(tlX-10), int(trX-10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        
        #calculate midpoints for left-right of rectangle
        (tlX, trX) = midPoint(tl, bl)
        (brX, blX) = midPoint(tr, br)
        
        #draw midpoint dots for left and right
        cv2.circle(cont_img, (int(tlX), int(trX)), 1, (255, 0, 0), 2)
        cv2.circle(cont_img, (int(brX), int(blX)), 1, (255, 0, 0), 2)
        
        #connect the midpoints using line
        cv2.line(cont_img, (int(tlX), int(trX)), (int(brX), int(blX)), (255, 255, 255), 1)
        
        #calculate the distance based on midpoints
        dB = dist.euclidean((tlX, trX), (brX, blX))
        
        #print the size in pixel in each contour rectangle
        cv2.putText(cont_img, "{:.1f} px".format(dB), (int(brX+10), int(blX+10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
        
        
    #show processed image with contour printed
plt.figure(figsize=(15,15))
plt.imshow(cont_img)
plt.show()
data = Image.fromarray(cont_img)
data.show('title')
