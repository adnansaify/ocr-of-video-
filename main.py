import cv2
import pytesseract
import numpy as np
import itertools
import os
import math

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

count = 1
vid = "LG.mp4"
vidcap = cv2.VideoCapture(vid)
sec = 0


def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            newpath = "Frames"
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            cv2.imwrite("Frames\Frames" + str(count) + ".jpg", image)
        return hasFrames

frameRate = 0.5
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)


myPath = os.path.abspath('Frames')

# initializing the number of files in the photos folder
num = 0

items = os.listdir(myPath)

for item in items:
  if os.path.isfile(os.path.join(myPath, item)):
    num = num + 1


print(num)

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_threshold(img, argument):
    switcher = {
        1: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        2: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        3: cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    }
    return switcher.get(argument, "Invalid method")

kernel=np.ones((1,1),np.uint8)

def apply_noise_removal(img, argument):
    switcher = {
        1: cv2.blur(img, (5, 5)),
        2: cv2.GaussianBlur(img, (5, 5), 0),
        3: cv2.medianBlur(img, 5),
        4: cv2.bilateralFilter(img, 9, 75, 75),
        5: cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel),
        6: cv2.erode(img,kernel,iterations=1)
    }
    return switcher.get(argument, "Invalid method")


list1 = [1, 2, 3]
list2 = [1, 2, 3, 4, 5, 6]
all_combo = []
for i in list1:
    for j in list2:
        temp = []
        temp.append(i)
        temp.append(j)
        all_combo.append(temp)


for j in range(1, num):
    for i in all_combo:
        # Give Path to read images
        img = cv2.imread("Frames\Frames%s.jpg" % str(j))

        img=get_grayscale(img)
        img = apply_threshold(img, i[0])
        img = apply_noise_removal(img, i[1])

        name = str(i[0]) + "," + str(i[1])
        newpath = "Outputs\img%s" % str(j)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        cv2.imwrite("Outputs\img%s\%s.jpg" % (str(j), name), img)

        myconfig = r" --psm 6 --oem 3"
        text = pytesseract.image_to_string(img, config=myconfig)
        f = open("Outputs\img%s\%s.txt" % (str(j), name), "w+")
        f.write(text)
        f.close()
