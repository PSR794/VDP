import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def nothing(x):
    pass
#Window for drawing, which has trackbars for changing colours
cv.namedWindow('Drawing Board')

cv.createTrackbar("R", "Drawing Board", 0, 255, nothing)
cv.createTrackbar("G", "Drawing Board", 0, 255, nothing)
cv.createTrackbar("B", "Drawing Board", 0, 255, nothing)
cv.createTrackbar("Size", "Drawing Board", 3, 30, nothing)

#The main window
cv.namedWindow("Trackbars")
#Trackbars to change the hsv upper and lower limits
cv.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera')
    exit()

kernel = np.ones((3,3), dtype=np.uint8)
global hold_flag
points = []
cont_flag=0

while True:
    ret, frame = cap.read()
    if not ret :
        print("Can't recieve frame, try again later maybe...")
        break
    frame = cv.flip(frame,1)

    #Trackbars to get the range of stylus
    l_h = cv.getTrackbarPos("L - H", "Trackbars")
    l_s = cv.getTrackbarPos("L - S", "Trackbars")
    l_v = cv.getTrackbarPos("L - V", "Trackbars")
    u_h = cv.getTrackbarPos("U - H", "Trackbars")
    u_s = cv.getTrackbarPos("U - S", "Trackbars")
    u_v = cv.getTrackbarPos("U - V", "Trackbars")
    
    lower_col = np.array([l_h,l_s,l_v])
    upper_col = np.array([u_h,u_s,u_v])
    
    #creating mask
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_col,  upper_col)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    masked_img = cv.bitwise_and(frame, frame, mask = mask)
    cv.imshow('Trackbars',masked_img)

    #Pressing enter to create contour
    if cv.waitKey(10)&0xff==13 or cont_flag==1:
        #creating the contour
        cnt,_ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cont_flag=1

        if len(cnt)>0:
            c = max(cnt, key = cv.contourArea) #finding contour with max area
            #drawing a rectangle around
            rect = cv.minAreaRect(c)
            global cx,cy
            [(cx,cy),(w,h),_] = rect
            box = cv.boxPoints(rect)
            box = np.int0(box)
            cv.drawContours(masked_img,[box],0,(0,0,255),2)
            #circle showing the middle
            cv.circle(masked_img,(int(cx),int(cy)),3,(255,0,0),-1)
            cv.imshow('Trackbars', masked_img)
            
            #making a board to draw
            board = np.zeros(frame.shape, np.uint8)
            board[:] = [255,255,255]

            r = cv.getTrackbarPos("R", "Drawing Board")
            g = cv.getTrackbarPos("G", "Drawing Board")
            b = cv.getTrackbarPos("B", "Drawing Board")
            sz = cv.getTrackbarPos("Size", "Drawing Board")
    else:
        continue
    
    cv.circle(board,(int(cx),int(cy)),sz,(b,g,r),-1)
    #Stops writing when 'p' is pressed
    if cv.waitKey(40)&0xff==ord('p'):
        points.append((0,0))
    else:
        points.append((int(cx), int(cy)))
    #Draw for all the points
    for i in range(1,len(points)):
        if points[i]==(0,0):
            pass
        else:
            if points[i-1]==(0,0):
                pass
            else:
                cv.line(board,points[i-1],points[i],(b,g,r),sz)
            cv.imshow('Drawing Board', board)
            
    if cv.waitKey(1)&0xff == 27:
        break
    #Clear the board when pressed 'c'
    if cv.waitKey(5)&0xff == ord('c'):
        points[:]=[]
        continue

cap.release()
cv.destroyAllWindows()
