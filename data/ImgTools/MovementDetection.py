import cv2
import pandas
from ImgTools.TimeClass import Timer
import math
from datetime import datetime

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

