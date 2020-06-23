# Imports
import numpy as np
import cv2
import math

# 얼굴과  검출을 위한 케스케이드 분류기 생성 
#OpenCV의 상위 레벨 API 
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')


# 카메라 캡쳐 활성화
# 웹 카메라는 0번!
cap = cv2.VideoCapture(0)

#얼굴 인식 될 때 사각형의 좌표값 출력하기 위해 정의
centerw=0
centerh=0

#실시간으로 좌표 출력하기엔 너무 많은 좌표가 출력되기에 time 이 50 이 될때마다 출력 하기 위해 정의
time=0

while cap.isOpened():    
    ret, img = cap.read()  # 프레임 읽기
    center = 0
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 얼굴 검출    
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(80,80))
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255,0),2)
            
            centerw = (x+w)/2
            centerh = (y+h)/2
            
            roi = gray[y:y+h, x:x+w]
        cv2.imshow('face detect', img)
        time=time+1
        print
        if(time==50):
            print('(',centerw,centerh,')')
            time=0
    else:
        break
    if cv2.waitKey(5) == 27: #키보드 esc 눌러주세용
        break
        
cap.release()
cv2.destroyAllWindows()