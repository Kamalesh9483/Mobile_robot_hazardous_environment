#detect irregular shape and contour area and print size
import cv2
import os

mainFolder = 'Image Stitching'
myFolders = os.listdir(mainFolder)
print(myFolders)

#search through folders to retrieve images
for folder in myFolders:
    path = mainFolder + '/' + folder
    print(path)
    images = []
    myList = os.listdir(path)
    print(f' Total no. of images detected {len(myList)}')
    for imgN in myList:
        curImg = cv2.imread(f'{path}/{imgN}')
        curImg = cv2.resize(curImg, (0,0), None, 0.3, 0.3)
        images.append(curImg)
        cv2.imshow('curImg',curImg )
        cv2.waitKey(0)
    
# dim = (1024,768)
# left = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
# left = cv2.resize(left, dim, interpolation=cv2.INTER_AREA)
# right = cv2.imread('2.jpg', cv2.IMREAD_COLOR)
# right = cv2.resize(right, dim, interpolation=cv2.INTER_AREA)
# images = []
# images.append(left)
# images.append(right)
    
# Image stitching 
# stitcher = cv2.Stitcher.create()
stitcher = cv2.Stitcher.create()
(ret, pano) = stitcher.stitch(images)
if (ret == cv2.STITCHER_OK):
    print('Panaroma Generated')
    cv2.imshow('Panaroma', pano)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('Panaroma generation unsuccesful')
