from cv2 import imdecode
import cv2
import requests
import sqlite3
import numpy as np
import cv2
import imutils # image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges, 
import imutils.perspective as persp # order contour cordinates - left, right, top, bottom
import scipy.spatial.distance as dist # to find distance
import matplotlib.pyplot as plt
import numpy as np
import os
import time

def empty(a):
    pass

def imageProcessor(dummy, rawImageQueue, outPutImageQueue):
    # url = "http://192.168.29.168:81/stream"
    url = "http://192.168.43.140:81/stream"
    n = 1

    # Creating Trackbar for colour detection
    cv2.namedWindow("Trackbar")
    cv2.resizeWindow("Trackbar",640,640)



    # Setting HUE, SATURATION, VALUE min and max values
    cv2.createTrackbar("thresh Min","Trackbar", 150, 200, empty)
    cv2.createTrackbar("thresh Max","Trackbar", 155, 255, empty)
    cv2.createTrackbar("kernel Min","Trackbar", 0, 50, empty)
    cv2.createTrackbar("kernel Max","Trackbar", 0, 50, empty)
    cv2.createTrackbar("itr_dilation","Trackbar", 0, 10, empty)
    cv2.createTrackbar("itr_erosion","Trackbar", 0, 10, empty)
    # cv2.createTrackbar("gauss_blur","Trackbar", 0, 7, empty)
    # cv2.createTrackbar("canny_l","Trackbar", 0, 100, empty)
    # cv2.createTrackbar("canny_u","Trackbar", 0, 100, empty)
    
    r = requests.get(url, stream=True)
    boundary = bytes('\r\n--123456789000000000000987654321\r\nContent-Type: image/jpeg\r\nContent-Length: ', 'utf-8')
    for line in r.iter_lines(delimiter=boundary):
        if line:
            if n!=0:
                pictureArray = bytearray(line)
                # print(pictureArray)
                # with open("./stream_images/image{}.jpg".format(n), "wb") as binary_file:
                # Write bytes to file
                img = imdecode(np.asarray(bytearray(pictureArray[8:])), cv2.IMREAD_COLOR)
                if img is None:
                    continue 

                img_original = img 
                            
                # #convert image to gray scale for detecting the contours
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                
                # # Getting Trackbar control
                thresh_min = cv2.getTrackbarPos("thresh Min","Trackbar")
                thresh_max = cv2.getTrackbarPos("thresh Max","Trackbar")
                kernel_min = cv2.getTrackbarPos("kernel Min","Trackbar")
                kernel_max = cv2.getTrackbarPos("kernel Max","Trackbar")
                itr_dil = cv2.getTrackbarPos("itr_dilation","Trackbar")
                itr_ero = cv2.getTrackbarPos("itr_erosion","Trackbar")
                # gaussian_blur = cv2.getTrackbarPos("gauss_blur","Trackbar")
                # cannyfilter_l = cv2.getTrackbarPos("canny_l","Trackbar")
                # cannyfilter_u = cv2.getTrackbarPos("canny_u","Trackbar")

                thresh, thresh_img = cv2.threshold(gray, thresh_min, thresh_max, cv2.THRESH_BINARY) # cv2.threshold(gray, thresh value, brightness, cv2.THRESH_BINARY)
                kernel = np.ones((kernel_min, kernel_max), np.uint8)
                img_dilation = cv2.dilate(thresh_img, kernel, iterations= itr_dil)
                img_erosion = cv2.erode(img_dilation, kernel, iterations= itr_ero)
                
                
                # cv2.imshow("Threshed",img_erosion)
                print("Hello world from put1")
                rawImageQueue.put(img_erosion)


                # find the total contours
                conts = cv2.findContours(img_erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # print('Total number of contours using cv2 are ', len(conts))
                #fine tune contours by cv2 using imutils
                conts = imutils.grab_contours(conts)
                # print('Total number of contours using imutils are ', len(conts))


                #create empty image with original dimension
                cont_img = np.zeros(img.shape)

                #draw the contours in the empty image - cont_img
                cont_img = cv2.drawContours(img_original, None , -1, (0,0,0), 1)


                #midpoint definition
                def midPoint(ptA, ptB):
                    return ((ptA[0] + ptB[0])/2, (ptA[1] + ptB[1])/2)

                # #loop over all the contour coordinates
                for c in conts:
                    # extract box points
                    box = cv2.minAreaRect(c) #(left, top), (right, bottom), accuracy 
                    # print(box)
                    box = cv2.boxPoints(box)
                    #convert box points to integer
                    box = np.array(box, dtype='int')
                    
                    if cv2.contourArea(c) < 500:
                        continue
                        
                    #draw contour
                
                    # cv2.drawContours(cont_img, [c], -1, (0,255,0), 1)
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
                        
                # cv2.imshow("Cont_img",cont_img)
                outPutImageQueue.put(cont_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                #         #show processed image with contour printed
                #         # plt.figure(figsize=(15,15))
                # cv2.imshow("Final_img", cont_img)
                # plt.show()
                # filename = './edited_images/savedImage{}.jpg'.format(n)
                # cv2.imwrite(filename, img)   
            
                
                # cv2.waitKey(0)
                # binary_file.write(pictureArray[8:])
                # n=n+1
                # if n==100:
                    # break
                
