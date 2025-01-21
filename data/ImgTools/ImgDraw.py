import cv2
import scipy.ndimage
import numpy as np

class ImgDraw:
    def __init__(self, img_name, dir='IMGS'):
        self.img_name = img_name
        self.img = cv2.imread(f'./{dir}/{img_name}')
        self.img_a = self.img
        self.dir = dir

    def display(self):
        running = True
        
        while running:
            key = cv2.waitKey(1)
            cv2.imshow(f"{self.img_name}", self.img_a)
            
            if key == ord("q"):
                running = False
            elif key == ord("1"):
                self.reset()
                self.gray()
            elif key == ord("2"):
                self.reset()
                self.graye()
            elif key == ord("3"):
                self.reset()
                self.fun()
            elif key == ord("4"):
                self.reverse()
            elif key == ord("5"):
                self.reset()
                self.draw()
            elif key == ord("6"):
                self.mirror()
            elif key == ord("8"):
                self.save()
            elif key == ord("9"):
                self.reset()

        cv2.destroyAllWindows()
        
    def grayscale(self):
        return np.dot(self.img_a[..., :3], [1, 1, 1])
    
    def dodge(self, front, back):
        result = front * 255/(255 - back + 1)
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
        
    def red(self):
        red = self.img_a
        red = red[:, :, 0]
        self.img_a = red
        
    def green(self):
        green = self.img_a
        green = green[:, :, 1]
        self.img_a = green

    def blue(self):
        blue = self.img_a
        blue = blue[:, :, 2]
        self.img_a = blue

    def graye(self):
        gray = self.img_a.T
        self.img_a = gray[-1::].T

    def gray(self):
        self.img_a = cv2.cvtColor(self.img_a, cv2.COLOR_BGR2GRAY)

    def reverse(self):
        self.img_a = np.flipud(self.img_a)

    def save(self, name=None):
        if name is None:
            cv2.imwrite(f'./{self.dir}/{self.img_name}', self.img_a)
        else:
            cv2.imwrite(f'./{self.dir}/{name}', self.img_a)
            
    def resize(self, width, height):
        self.img_a = cv2.resize(self.img_a, (width, height))

    def reset(self):
        self.img_a = self.img

    def mirror(self):
        mirror = np.fliplr(self.img_a)
        # self.img_a = funny.T
        self.img_a = mirror
