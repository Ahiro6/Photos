import cv2
import pandas
from ImgTools.TimeClass import Timer
import math
from datetime import datetime

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

