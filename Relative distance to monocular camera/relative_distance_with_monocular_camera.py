'''
Code part of the article "Visual Inertial Navigation System for a Jetbot Robotic Mobile Platform"
'''

import cv2
import numpy as np

area = 1
global x

# Specifying upper and lower ranges of color to detect in hsv format
lower = np.array([15, 150, 20])
upper = np.array([35, 255, 255]) # (These ranges will detect Yellow)
w=0

# Capturing webcam footage
webcam_video = cv2.VideoCapture(0)

#Main Code

while True :
    
    x=0
    y=0
    w=0
    h=0

    success, video = webcam_video.read() # Reading webcam footage

    img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img, lower, upper) # Masking the image to find the color

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                area = (w * h)
                cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangles
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), 3)
                
    distance=((6.66*(area**(-0.0652)))+(-2.966))*100 #Calculate distance on centimeters based on area of pixels

    # When the object its determined to be further than a meter
    if (distance >= 100):
        cm = round(distance/100,2)
        value = str(cm)
        cv2.putText(video,value,(x,y),cv2.FONT_HERSHEY_TRIPLEX,5,(255,180,180),10)
        cv2.putText(video,"m",(x+70,y+70),cv2.FONT_HERSHEY_PLAIN,5,(255,180,180),10)
        print(cm,"m")

    # When the object its determined to be closer than a meter    
    if (distance < 100):
        cm = int(distance)
        value = str(cm)
        cv2.putText(video,value,(x,y),cv2.FONT_HERSHEY_TRIPLEX,5,(255,180,180),10)
        cv2.putText(video,"cm",(x+70,y+70),cv2.FONT_HERSHEY_PLAIN,5,(255,180,180),10)
        print(cm, "cm")
    


    cv2.imshow("mask image", img) # Displaying mask image

    cv2.imshow("HSV", video) # Displaying webcam image
    
    cv2.imshow("Gray", mask) # Displaying grey image

# To close the window, press the Q key on the keyboard

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()