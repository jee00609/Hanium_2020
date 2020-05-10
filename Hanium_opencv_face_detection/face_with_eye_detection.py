# Imports
import numpy as np
import cv2
import math

# 얼굴과  검출을 위한 케스케이드 분류기 생성 
#OpenCV의 상위 레벨 API 
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')

#---얼굴 및 눈 검출

# 카메라 캡쳐 활성화
# 웹 카메라는 0번!
cap = cv2.VideoCapture(0)

while cap.isOpened():    
    ret, img = cap.read()  # 프레임 읽기
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 얼굴 검출    
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(80,80))
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255,0),2)
            roi = gray[y:y+h, x:x+w]
            # 눈 검출
            eyes = eye_cascade.detectMultiScale(roi)
            for i, (ex, ey, ew, eh) in enumerate(eyes):
                if i >= 2:
                    break
                cv2.rectangle(img[y:y+h, x:x+w], (ex,ey), (ex+ew, ey+eh), (255,0,0),2  )
        cv2.imshow('face detect', img)
    else:
        break
    if cv2.waitKey(5) == 27: #키보드 esc 눌러주세용
        break
        
cap.release()
cv2.destroyAllWindows()