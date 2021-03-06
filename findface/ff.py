#!/usr/bin/python

import numpy as np
import cv2

haar_cascade_home='/usr/local/Cellar/opencv/2.4.6.1/share/OpenCV/haarcascades/'

def hc(p):
    return haar_cascade_home + p

face_cascade = cv2.CascadeClassifier(hc('haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(hc('haarcascade_eye.xml'))

img = cv2.imread('../tests/images/lena1.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

