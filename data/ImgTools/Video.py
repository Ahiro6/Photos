import numpy as np
import cv2
# import imageio
import scipy.ndimage
import time
from datetime import datetime
# import requests
import pandas
# import os
import math


from ImgTools.FaceDetection import FaceDetection
from ImgTools.ImgDraw import ImgDraw
from ImgTools.MovementDetection import MovementDetection

class Video:
    def __init__(self, dir='IMGS'):
        self.frame = None
        self.video = cv2.VideoCapture(0)
        self.detect = False
        self.mask = None
        
        self.img_name = None
        self.dir = dir

        self.face = FaceDetection()
        self.move = MovementDetection()

    def read_frame(self):
        check, self.frame = self.video.read()
        self.detect_face()
    
    def detect_face(self):
        if self.detect:
            self.face.detect_face(self.frame, self.mask)
            
    def release(self):
        self.video.release()

    def run(self, name, save_data=False):
        running = True
        
        while running:

            self.read_frame()

            key = cv2.waitKey(1)
            cv2.imshow(name, self.frame)

            if key == ord('q'):
                running = False

            elif key == ord('p'):
                print('Picture taken')
                self.save_img()
                
            elif key == ord('0'):
                self.no_mask()

            elif key == ord("1"):
                self.plain_mask()

            elif key == ord("2"):
                self.bat_mask()

            elif key == ord("3"):
                self.flash_mask()

        if save_data:
            self.move.save()
            self.face.save()

        self.release()
        cv2.destroyAllWindows()
        
    def no_mask(self):
        self.detect = False
        self.mask = None
        
    def bat_mask(self):
        self.detect = True
        self.mask = cv2.imread("./Assets/Batman.png", 1)
  
    def flash_mask(self):
        self.detect = True
        self.mask = cv2.imread("./Assets/Flash.png", 1)
            
    def plain_mask(self):
        self.detect = True
        self.mask = None
            

    def save_img(self):
        self.detect_face()
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.img_name = f"IMG_{timestr}.png"
        cv2.imwrite(f'./{self.dir}/{self.img_name}', self.frame)
        
    def edit(self):
        img_ed = ImgDraw(self.img_name, dir=self.dir)
        img_ed.display()

         

