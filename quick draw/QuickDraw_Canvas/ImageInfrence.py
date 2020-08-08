import cv2
import os.path

from keras.models import load_model
import numpy as np
from collections import deque
import os

from playsound import playsound

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


model = load_model('QuickDraw.h5')
file = 'saveImage\\image.png'
emojis = get_QD_emojis()


if os.path.isfile(file):
    print("Yes. it is a file")
    src = cv2.imread(file, cv2.IMREAD_COLOR)
    dst = cv2.bitwise_not(src)
    
    cv2.imshow("src", src)
#     cv2.imshow("dst", dst)
    
    blackboard_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.medianBlur(blackboard_gray, 1)
    blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)

    #https://hoony-gunputer.tistory.com/entry/opencv-python-%EC%9D%B4%EB%AF%B8%EC%A7%80-Thresholding
    #검은 화면에 사용자가 그린 흰색선이 존재하는 이미지가 뜰 것
    thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     cv2.imshow("thresh",thresh1)
    
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
#             img = cv2.imread("qd_emo/0.png", cv2.IMREAD_COLOR)
            img = cv2.imread(result, cv2.IMREAD_COLOR)
            cv2.imshow("img",img)
            playsound('saveAudio\\sampleAudio.mp3')

    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
elif os.path.isdir(file):
    print("Yes. it is a directory")
elif os.path.exists(file):
    print("Something exist")
else :
    print("Nothing")