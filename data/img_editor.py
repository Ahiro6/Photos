import numpy as np
import cv2
# import imageio
import scipy.ndimage
import time
from datetime import datetime
# import requests
import pandas
# import os
from TimeClass import Timer
import math


class ImgDraw:
    def __init__(self, img):
        self.img = img
        self.img_a = self.img

    def grayscale(self):
        return np.dot(self.img_a[..., :3], [1, 1, 1])

    def dodge(self, front, back):
        result = front * 255 / (255 - back + 1)
        result[result > 255] = 255
        result[back == 255] = 255
        return result.astype('uint8')

    def draw(self):
        # For drawing picture
        gray = self.grayscale()
        negative = 255 - gray
        filte = scipy.ndimage.filters.gaussian_filter(negative, sigma=10)
        self.img_a = self.dodge(gray, filte)

    def fun(self):
        funny = self.img_a.T
        funny = funny[::-1]
        self.img_a = funny.T

    def graye(self):
        gray = self.img_a.T
        self.img_a = gray[-1::].T

    def gray(self):
        self.img_a = cv2.cvtColor(self.img_a, cv2.COLOR_BGR2GRAY)

    def reverse(self):
        self.img_a = np.flipud(self.img_a)

    def save(self, name):
        cv2.imwrite(name + ".png", self.img_a)

    def resize(self, width, height):
        self.img_a = cv2.resize(self.img_a, (width, height))

    def reset(self):
        self.img_a = self.img

    def mirror(self):
        mirror = np.fliplr(self.img_a)
        # self.img_a = funny.T
        self.img_a = mirror


class FaceDetection:
    def __init__(self):
        self.status_list = []
        self.times = []
        self.counter = Timer()
        self.df = pandas.DataFrame(columns=["Date", "Day", "Start", "End", "Times"])

    def detect_face(self, img, img_face):
        status = 0
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_cas = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cas.detectMultiScale(img_gray, scaleFactor=1.15, minNeighbors=4)

        if img_face is not None:
            if len(faces) > 0:
                for x, y, w, h in faces:
                    status = 1
                    roi = img[y: y + h, x: x + w]
                    img_face = cv2.resize(img_face, (int(w * 1.65), int(h * 1.80)))
                    fh, fw, fc = img_face.shape
                    for i in range(0, fh):
                        for j in range(0, fw):
                            if img_face[i, j][2] > 0:
                                img[y + int(i - h / 2.7), x + int(j - w / 3)] = img_face[i, j]

        else:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cas = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            faces = face_cas.detectMultiScale(img_gray, scaleFactor=1.15, minNeighbors=4)

            if len(faces) > 0:
                for x, y, w, h in faces:
                    status = 1
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if len(self.status_list) > 1:
            if self.status_list[-1] == 1 and self.status_list[-2] == 0:
                self.times.append(datetime.now().strftime("%x"))
                self.times.append(datetime.now().strftime("%a"))
                self.times.append(datetime.now())
                self.counter.start()
            if self.status_list[-1] == 0 and self.status_list[-2] == 1:
                self.times.append(datetime.now())
                self.counter.stop()
                self.times.append(math.ceil(self.counter.elapsed_time))

        self.status_list.append(status)

    def save(self):
        if len(self.times) % 5 != 0:
            self.times.append(datetime.now())
            self.counter.stop()
            self.times.append(math.ceil(self.counter.elapsed_time))
        for i in range(0, len(self.times), 5):
            self.df = self.df.append(
                {"Date": self.times[i], "Day": self.times[i + 1], "Start": self.times[i + 2],
                    "End": self.times[i + 3],
                    "Times": self.times[i + 4]}, ignore_index=True)
        self.df.to_csv("Times_Face.csv")


class MovementDetection:
    def __init__(self):
        self.first = None
        self.status_list = []
        self.times = []
        self.counter = Timer()
        self.df = pandas.DataFrame(columns=["Date", "Day", "Start", "End", "Times"])

    def detect_move(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        status = 0

        if self.first is None:
            self.first = gray

        delta = cv2.absdiff(self.first, gray)
        thresh = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) < 10000:
                continue
            status = 1
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)

        if len(self.status_list) > 1:
            if self.status_list[-1] == 1 and self.status_list[-2] == 0:
                self.times.append(datetime.now().strftime("%x"))
                self.times.append(datetime.now().strftime("%a"))
                self.times.append(datetime.now())
                self.counter.start()
            if self.status_list[-1] == 0 and self.status_list[-2] == 1:
                self.times.append(datetime.now())
                self.counter.stop()
                self.times.append(math.ceil(self.counter.elapsed_time))

        self.status_list.append(status)

    def save(self):
        if len(self.times) % 5 != 0:
            self.times.append(datetime.now())
            self.counter.stop()
            self.times.append(math.ceil(self.counter.elapsed_time))
        for i in range(0, len(self.times), 5):
            self.df = self.df.append(
                {"Date": self.times[i], "Day": self.times[i + 1], "Start": self.times[i + 2], "End": self.times[i + 3],
                 "Times": self.times[i + 4]}, ignore_index=True)
        self.df.to_csv("Times_movement.csv")


class Video:
    def __init__(self):
        self.url = ""
        self.running = True
        self.video = cv2.VideoCapture(0)
        self.detect = [False, True]
        self.frame = self.video.read()
        self.mask = None

        self.face = FaceDetection()
        self.move = MovementDetection()

    def run(self, name, edit=False, save_data=False, save_img=False):
        while self.running:

            check, self.frame = self.video.read()

            if self.detect[0]:
                self.move.detect_move(self.frame)
                self.face.detect_face(self.frame, self.mask)

            key = cv2.waitKey(1)
            cv2.imshow(name, self.frame)

            if key == ord('q'):
                self.running = False

            elif key == ord('p'):
                cv2.imwrite("1.jpg", self.frame)

            elif key == ord("f"):
                self.detect[0], self.detect[1] = self.detect[1], self.detect[0]

            elif key == ord("1") and self.detect[0]:
                self.mask = cv2.imread("Batman.png", 1)

            elif key == ord("2") and self.detect[0]:
                self.mask = cv2.imread("Flash.png", 1)

            elif key == ord("3") and self.detect[0]:
                self.mask = None

        if save_data:
            self.move.save()
            self.face.save()

        if save_img:
            timestr = time.strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(timestr + ".png", self.frame)
        self.video.release()
        cv2.destroyAllWindows()

        if edit:
            img_ed = ImgDraw("1.jpg")

            while True:
                key = cv2.waitKey(1)
                cv2.imshow(name, img_ed.img_a)

                if key == ord("q"):
                    break
                elif key == ord("1"):
                    img_ed.gray()
                elif key == ord("2"):
                    img_ed.graye()
                elif key == ord("3"):
                    img_ed.fun()
                elif key == ord("4"):
                    img_ed.reverse()
                elif key == ord("5"):
                    img_ed.draw()
                elif key == ord("6"):
                    img_ed.mirror()
                elif key == ord("7"):
                    width = int(input("Width"))
                    height = int(input("Height"))
                    img_ed.resize(width, height)
                elif key == ord("8"):
                    timestr = time.strftime("%Y%m%d_%H%M%S")
                    img_ed.save(f"Edit{timestr}")
                elif key == ord("9"):
                    img_ed.reset()

            cv2.destroyAllWindows()


video = Video()
video.run("Test", save_data=True)
