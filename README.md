# VIRTUAL DRAWING PAD
The aim is to let the user draw on a virtual pad provided by moving a stylus in front of the webcam. The task uses the basics of Python module- OpenCV and Numpy.
Image segmentation technique (separating the stylus from the frame) helps in solving the problem.


---
---

## THE PROCESS
* The HSV mask of the captured frame is used for extracting the region of interest (the stylus).
* We get a BGR frame of the stylus whose grayscale form is necessary for further processes.
* For the stylus to get tracked, it is necessary to get an edge image of it for which the grayscale form of the frame mentioned above, passed as the argument.
* Obtaining a perfect edge is essential, so we denoise the image by  "Opening", a morphological transformation that carries out erosion followed by dilation to curb the background noises captured because of the range selected to detect the stylus.
* The edge image of the following was found with Canny edge detection. In the next step, we get the contours points to follow the stylus.
* After getting the contour points, we use the `cv2.minEnclosingCircle` to find its position in the frame.
* As the contour keeps fluctuating in between, probability of getting small circles increases so we put a threshold for the radius to be displayed and to take that position(center of the circle) into consideration.
* A circle is drawn by `cv2.circle` function on the white image declared before the main loop on the corresponding point of the white image (the drawing pad).
* The code stops drawing when the user hides the stylus and continues when it is shown again to the camera.



---


---

## THE MASK LIMITATION
1.  The HSV range used is only valid for the stylus used for testing the code.
1. Both the thresholds are to be set manually by the user.
1. The background should not consist of something other than the stylus similar to the shade of it in the capture frame for better results.
1. Brightness factor affects a lot as avoiding the BGR range gives the algorithm an advantage of identifying a unique shade but, changing the light conditions may hamper the mask and bring the noise in it.
1. Though a suitable range of HSV can tackle it, the probability of other background noises getting caught in the act rises. Hence the third point should be noted carefully.
example is given below-

![](https://i.imgur.com/9fVA61K.jpg) 
> *here is a mask set on normal room lightings*
---
![](https://i.imgur.com/kb5tniu.jpg)
> here is a same mask for the same stylus in different lighting conditions
> 
---
---

### THE STYLUS
A a green pen cap was used as a stylus for the testing.

![](https://i.imgur.com/MgrLU6a.jpg)

---
---

### RESULTS
Given below is the video, shows the final code in action.
https://drive.google.com/file/d/1IpHWfHIVJzGFdHSEiqWWKS-3U83H5qr5/view?usp=drivesdk
---

LANGUAGE VERSIONS:
1. Python 3.7 
2. OpenCV 4.2.0
3. numpy 1.19.0
