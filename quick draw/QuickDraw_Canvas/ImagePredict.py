import cv2
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *

import os.path
from keras.models import load_model
import numpy as np
from collections import deque
import os
from playsound import playsound

from PIL import ImageTk,ImageGrab

width = 400
height = 400
center = height//2
white = (255, 255, 255)
green = (0,128,0)

width2 = width*2
height2 = height*2

def save():
    # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
    # filename = "my_drawing.png"
    # image1.save(filename)
    #놔두긴 했는데 지워도 될듯
    filename = "saveImage\\MyDraw.png"
    image.save(filename)
    
def clear():
    #이거 제대로 안됨 -- 2020-08-17
    cv.delete ( "all")
    image = PIL.Image.new("RGB", (width, height), white)
    draw = ImageDraw.Draw(image)
    
def predict():
    filename = "saveImage\\image.png"
    image.save(filename)
    
    model = load_model('QuickDraw.h5')
    file = 'saveImage\\image.png'
    emojis = get_QD_emojis()


    if os.path.isfile(file):
        print("Yes. it is a file")
        src = cv2.imread(file, cv2.IMREAD_COLOR)
        dst = cv2.bitwise_not(src)

        blackboard_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.medianBlur(blackboard_gray, 1)
        blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)

        thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        blackboard_cnts= cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        if len(blackboard_cnts) >= 1:
            cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                digit = blackboard_gray[y:y + h, x:x + w]
                pred_probab, pred_class = keras_predict(model, digit)
                #여기서 pred_class 는 각이미지의 번호를 나타내는듯
                print("hey!",pred_probab," and ", pred_class)
                result_path1 = 'qd_emo\\'
                result_path2 = '.png'
                result = result_path1+str(pred_class)+result_path2
                print(result)
                img = cv2.imread(result, cv2.IMREAD_COLOR)
                resultImage = ImageTk.PhotoImage(file=result)
                label.configure(image=resultImage)
                label.image = resultImage # keep a reference!
#                 print("DONE!")
                #2020-08-18 그림 인식 시 어떤 그림인지 텍스트로 표현
                if pred_class==0:
                    text.set("This is apple!")
                elif pred_class==1:
                    text.set("This is Bowtie!")
                

    elif os.path.isdir(file):
        print("Yes. it is a directory")
    elif os.path.exists(file):
        print("Something exist")
    else :
        print("Nothing")
        
def voice():
    model = load_model('QuickDraw.h5')
    file = 'saveImage\\image.png'
    emojis = get_QD_emojis()


    if os.path.isfile(file):
        print("Yes. it is a file")
        src = cv2.imread(file, cv2.IMREAD_COLOR)
        dst = cv2.bitwise_not(src)

        blackboard_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.medianBlur(blackboard_gray, 1)
        blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)

        thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        blackboard_cnts= cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        if len(blackboard_cnts) >= 1:
            cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                digit = blackboard_gray[y:y + h, x:x + w]
                pred_probab, pred_class = keras_predict(model, digit)
                if pred_class==0:
                    playsound('saveAudio\\sampleAudio.mp3')
                
    elif os.path.isdir(file):
        print("Yes. it is a directory")
    elif os.path.exists(file):
        print("Something exist")
    else :
        print("Nothing")

def paint(event):
    # python_green = "#476042"
    x1, y1 = event.x, event.y
    if cv.old_coords:
        x2, y2 = cv.old_coords
        cv.create_line(x1, y1, x2, y2, fill="black",width=5)
        draw.line([x1, y1, x2, y2],fill="black",width=5)
    cv.old_coords = x1, y1
    
def reset_coords(event):
    cv.old_coords = None
    
###

def keras_predict(model, image):
    print("function keras_predict start")
    processed = keras_process_image(image)
    print("processed: " + str(processed.shape))
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def keras_process_image(img):
    print("function keras_process_image start")
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img

def get_QD_emojis():
    print("function get_QD_emojis start")
    emojis_folder = "qd_emo/"
    emojis = []
    for emoji in range(len(os.listdir("qd_emo/"))):
        print(emoji)
        emojis.append(cv2.imread(emojis_folder + str(emoji) + '.png', -1))
    return emojis

root = Tk()
root.geometry("800x420")

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.old_coords = None

# PIL create an empty image and draw object to draw on
# memory only, not visible
image = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)

#expand=True, fill="both"
cv.place(x=0, y=0, width=400, height=400)
cv.bind("<B1-Motion>", paint)
cv.bind("<ButtonRelease-1>", reset_coords)
root.bind("<Escape>", lambda e: root.destroy())

text= StringVar(root)
text.set("그림을 그리면 알아맞출게요!\n")
# text.configure(state="disabled")
textlabel = Label(root, textvariable=text)
textlabel.place(x=400, y=0, width=400, height=30)


predImage = ImageTk.PhotoImage(file="qd_emo\\1.png")
label=Label(root,image=predImage)
label.place(x=400, y=30, width=400, height=400)


button=Button(text="clear",command=clear)
button.place(x=0, y=400, width=100, height=20)

button=Button(text="save",command=save)
button.place(x=300, y=400, width=100, height=20)

button=Button(text="predict",command=predict)
button.place(x=150, y=400, width=100, height=20)

button=Button(text="voice",command=voice)
button.place(x=550, y=350, width=100, height=20)


root.mainloop()
