import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

pad=np.zeros((480,640,3),np.uint8) # creating the drawing pad
pad[::]=255
Max=0

img=np.zeros((300,300,3),np.uint8)#the color pallete image

#color pallete code
def nothing(x):
    pass

cv.namedWindow('image')

cv.createTrackbar('R','image',0,255,nothing)#red channel
cv.createTrackbar('G','image',0,255,nothing)#green channel
cv.createTrackbar('B','image',0,255,nothing)#blue channel
cv.createTrackbar('T','image',4,100,nothing)#thickness


vid=cv.VideoCapture(0) # starting video
kernel=np.ones((5,5),np.uint8) #kernel for morpholigical transforms
print('press esc to exit')
print('to move the stylus position hide it and shift at the other position')
if not vid.isOpened():
    print('camera didnt open')
    exit()
while True:
    cv.imshow('image',img)
    #position of track bars
    red=cv.getTrackbarPos('R','image')
    green=cv.getTrackbarPos('G','image')
    blue=cv.getTrackbarPos('B','image')
    thickness=cv.getTrackbarPos('T','image')
    img[:]=[blue,green,red]


    Return1,Frame=vid.read() #reading the frames
    hsv=cv.cvtColor(Frame,cv.COLOR_BGR2HSV)

    LR=np.array([0,179,116])
    HR=np.array([180,256,255])#setting the range for mask

    mask=cv.inRange(hsv,LR,HR)
    opening=cv.morphologyEx(mask,cv.MORPH_OPEN,kernel)
    dil=cv.dilate(opening,kernel,iterations=3)
    ring=cv.bitwise_and(Frame,Frame,mask=dil) # applying and operator to frames and mask to extract stylus

    ringray = cv.cvtColor(ring,cv.COLOR_BGR2GRAY)
    canny=cv.Canny(ringray,0,255) #canny edge detector for contour detection
    closing=cv.morphologyEx(canny,cv.MORPH_CLOSE,kernel) #for removing background noise
    contours,hierarchy=cv.findContours(closing,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)# fetching the contour coordinate
    
    if np.size(contours)==0:# case when user want to switch the position of stylus without drawing
        continue
    
    cnt=contours[0]
    (x,y),radius = cv.minEnclosingCircle(cnt)#stylus detection
    if radius>28:
        centre=(int(x),int(y))
        radius=int(radius)
        #marking the stylus
        cv.circle(Frame,centre,radius,(0,255,0),2)
        cv.circle(pad,centre,thickness,(blue,green,red),-1)
        cv.circle(pad,centre,thickness,(blue,green,red),-1)
        cv.imshow('DRAW',pad)
    cv.imshow('original',Frame)
    cv.imshow('thanosd',closing)
    cv.imshow('thanose',opening)
    cv.imshow('thanosf',dil)
    cv.imshow('canny',canny)
    k=cv.waitKey(3) & 0xFF
    if (cv.waitKey(1) & 0xFF==ord('q')) or k==27:
        break

#cleaning up
vid.release()
cv.destroyAllWindows()

