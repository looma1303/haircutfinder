import numpy as np
import cv2



img_src = cv2.imread("001.jpg")


img = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
img2 = img_src


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")


face_data = faceCascade.detectMultiScale(img, 

                     scaleFactor=1.1,

                     minNeighbors=1,

                     minSize=(40,40))  # 최소 얼굴 범위 40x40픽셀




cv2.namedWindow("image viewer1",cv2.WINDOW_NORMAL) 
cv2.imshow("image viewer1",img_src)

if len(face_data) > 0:
    print("FOUND")
    color = (0,0,255)
    for f in face_data:
        x,y,w,h = f
        eye_pic = face_data[y:y+h:,x:x+w]
        eyes = eyeCascade.detectMultiScale(img,1.1,3)
        cv2.rectangle(img2,(x,y),(x+w,y+h),color,thickness = 4)
        
        
        for e in eyes:
            color2 = (0,255,0)
            ex,ey,ew,eh = e
            cv2.rectangle(img2,(ex,ey),(ex+ew,ey+eh),color2,2)
            
    
    cv2.namedWindow("image viewer2",cv2.WINDOW_NORMAL)
    cv2.imshow("image viewer2",img2)
    
else:
    print("NOT FOUND")
    
cv2.waitKey(10000)
cv2.destroyAllWindows()