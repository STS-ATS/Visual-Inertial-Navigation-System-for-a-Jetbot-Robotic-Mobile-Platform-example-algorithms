'''
Code part of the article "Visual Inertial Navigation System for a Jetbot Robotic Mobile Platform"
'''

import cv2
import time 

'''
Its important to comment the section that will not be used, for example:
If you will use the camera, comment the section of the volunteer video, and so on.
'''
###################### Camera

#webcam_video = cv2.VideoCapture(0) #Conected Camera
#k=1

###################### Volunteer video

path = '<path_to_the_volunteer_video>'
k = 70
webcam_video = cv2.VideoCapture(path) #Volunteer Video

###################### Begin

prev_frame_time = 0
new_frame_time = 0

object_detector = cv2.createBackgroundSubtractorMOG2(2,200,detectShadows=False)

flag = 0


while True:

    success , video = webcam_video.read()
    
    gray = cv2.cvtColor(video,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    mask = object_detector.apply(blur)
    new_frame_time = time.time() 
    
    contours, a = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #Unpacking the contours dots
    for cnt in contours : 

        if contours is not None :
                  
            #cv2.drawContours(video,[cnt],-1, (0,250,0),2) #Original region contour
            iter = len(cnt)
            dots=[]
            if iter !=0 :
                None #If there is not movement, so there are no dots

            for n in cnt:
                x = cnt[0]
                x1 = x [0]
                x2 = x1[0]
                y = x1 [1]
                vect=(x2,y)
                cv2.circle(video,(x2,y),1,(200,255,100),thickness=1) #Shows the simplified version of the movement dots
                dots.append(vect)
                
    
    for n in range(0,len(dots)):
        f=dots[n]
        print(f) #Prints the dots coordinates on the region

    #Calculation of the frames            
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 
    fps = int(fps)
    fps = str(fps)
    
    cv2.putText(video, fps,(7, 70),cv2.FONT_HERSHEY_SIMPLEX, 3,(0, 200, 255), 3, cv2.LINE_AA) #Shows the number of frames on the corner
  
    cv2.imshow("Procesado", video) # Displaying webcam or video image

# To close the window, press the Q key on the keyboard

    if cv2.waitKey(k) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
