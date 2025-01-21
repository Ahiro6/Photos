import numpy as np
import cv2
import scipy.ndimage
from kivy.graphics.texture import Texture

img1 = "baymax.jpg"
img2 = "img.png"


class ImgDraw:
    def __init__(self, img):
        self.img = img
        self.img_a = cv2.imread(img, 1)
        cv2.imwrite("img.jpg", self.img_a)
        self.img = "img.jpg"

        self.pic_draw = self.draw()
        self.gray1_img = self.gray()
        self.gray2_img = self.grayscale(self.img_a)
        self.gray3_img = self.graye()
        self.funny = self.fun()
        self.revers = self.reverse()

    def grayscale(self, rgb):
        return np.dot(rgb[..., :3], [1, 1, 1])

    def dodge(self, front, back):
        result = front * 255/(255 - back + 1)
        result[result > 255] = 255
        result[back == 255] = 255
        return result.astype('uint8')

    def draw(self):
        # For drawing picture
        gray = self.grayscale(self.img_a)
        negative = 255 - gray
        filte = scipy.ndimage.filters.gaussian_filter(negative, sigma=10)
        draw = self.dodge(gray, filte)
        return draw

    def fun(self):
        funny = self.img_a.T
        funny = funny[::-1]
        funny = funny.T
        return funny

    def graye(self):
        gray = self.img_a.T
        gray = gray[-1::].T
        return gray

    def gray(self):
        gray_img = cv2.imread(self.img, 0)
        return gray_img

    def reverse(self):
        revers = cv2.imread(self.img, 1)
        revers = revers[::-1]
        return revers

    def save(self, name):
        cv2.imwrite(name + "1.jpg", self.gray1_img)
        cv2.imwrite(name + "2.jpg", self.gray2_img)
        cv2.imwrite(name + "3.jpg", self.gray3_img)
        cv2.imwrite(name+"_draw.jpg", self.pic_draw)
        cv2.imwrite(name + "_funny.jpg", self.funny)
        cv2.imwrite(name+"_reverse.jpg", self.revers)

    def reSize(self, img, width, height):
        img = cv2.resize(img, (width, height))
        return img


class FaceDetection:
    def __init__(self, img):
        # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cas = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cas.detectMultiScale(img, scaleFactor=1.10, minNeighbors=5)

        for x, y, w, h in faces:
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)


class Video:
    def __init__(self, width, height, target):
        # Texture.__init__(self, width, height, target)
        self.running = True
        video = cv2.VideoCapture(0)
        detect = [True, False]

        while self.running:

            check, self.frame = video.read()
            print(check)
            print(self.frame)

            if detect[0]:
                FaceDetection(self.frame)

            # cv2.imshow("Capture", self.frame)
            texture = Texture(width, height, target)
            texture.create(size=(width, height), colorfmt='bgr',
        bufferfmt='ubyte')
            texture.blit_buffer(self.frame,
                                size=(width-25, height-25),
                                pos=(0, 0),
                                colorfmt='bgr',
                                bufferfmt='ubyte',)
            key = cv2.waitKey(1)

        cv2.imwrite("1.jpg", self.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        video.release()


new2 = ImgDraw(img2)
face_detector = FaceDetection(new2.img_a)
new2.funny = new2.reSize(new2.funny, 1000, 300)
new2.save("ol-man")
