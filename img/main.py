import time
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.camera import Camera
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from hoverable import HoverBehavior
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import json
from datetime import datetime
from pathlib import Path
import glob
import random
from kivy.graphics.texture import Texture
import cv2
import img_editor
import time

Builder.load_file("design.kv")


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_in(self, username, password):
        with open("users.json", "r") as file:
            users = json.load(file)
        if username in users and users[username]["password"] == password:
            self.manager.current = "video_screen"
        else:
            self.ids.wrong.text = "Wrong username or password!"


class SignUpScreen(Screen):

    def add_user(self, username, password):
        with open("users.json", "r") as file:
            users = json.load(file)

        if username not in users:
            users[username] = {'username': username, 'password': password,
                               'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            with open("users.json", "w") as file:
                json.dump(users, file)
            print(users[username])
            self.manager.current = "success_screen"

        elif username in users:
            self.ids.taken.text = "This username is already taken."

    def cancel(self):
        self.manager.current = "login_screen"


class Success(Screen):

    def log_in(self):
        self.manager.current = "login_screen"


class VideoScreen(Screen):

    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        # self.ids.cam.play = False

    def take(self):
        self.ids.cam.export_to_png("1.png")
        # self.ids.cam.play = False
        self.manager.current = "photo_screen"


class PhotoScreen(Screen):

    def __init__(self, **kw):
        super(PhotoScreen, self).__init__(**kw)
        self.img_s = "1"
        self.img = Image()

        self.button = Button(text="Lets start")
        self.button.bind(on_press=self.start)
        self.button.size_hint = (1, 1)

        self.add_widget(self.button)
        # self.update()

    def start(self, instance):
        self.img_s = "1"

        # self.ids.photo.source = self.img

        self.img_a = cv2.imread(self.img_s + ".png", 1)
        self.edit = img_editor.ImgDraw(self.img_a)

        self.img.source = self.img_s + ".png"
        self.img.size_hint = (1, 1)

        self.remove_widget(self.button)
        self.add_widget(self.img)
        self.img.reload()

    def cancel(self):
        self.manager.current = "video_screen"
        self.add_widget(self.button)
        self.remove_widget(self.img)
        os.remove("1.png")

    def continu(self):
        self.edit.save(self.img_s)
        self.add_widget(self.button)
        self.remove_widget(self.img)
        self.manager.current = "edit_screen"

    def reset(self):
        self.edit.reSet()
        self.edit.save(self.img_s)
        self.img.reload()

    def one(self):
        self.edit.reSet()
        self.edit.draw()
        self.edit.save(self.img_s)
        self.img.reload()

    def two(self):
        self.edit.reSet()
        self.edit.fun()
        self.edit.save(self.img_s)
        self.img.reload()

    def three(self):
        self.edit.reSet()
        self.edit.gray()
        self.edit.save(self.img_s)
        self.img.reload()


class EditScreen(Screen):
    def __init__(self, **kw):
        super(Screen, self).__init__(**kw)
        self.img_s = "1"

        self.img2 = Image()

        self.button = Button(text="Lets start")
        self.button.bind(on_press=self.start)
        self.button.size_hint = (1, 1)

        self.add_widget(self.button)

    def start(self, instance):
        self.img_s = "1"

        self.img_a = cv2.imread(self.img_s + ".png", 1)
        self.edit = img_editor.ImgDraw(self.img_a)

        self.img2.source = self.img_s + ".png"
        self.img2.size_hint = (1, 1)

        self.remove_widget(self.button)
        self.add_widget(self.img2)
        self.img2.reload()

    def cancel(self):
        self.remove_widget(self.img2)
        self.add_widget(self.button)
        self.manager.current = "video_screen"
        os.remove("1.png")


    def continu(self):
        self.edit.save(self.img_s)
        self.remove_widget(self.img2)
        self.add_widget(self.button)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        os.rename(self.img_s + ".png", "Snap_{}".format(timestr) + ".png")
        self.manager.current = "video_screen"

    def reset(self):
        self.edit.reSet()
        self.edit.save(self.img_s)
        self.img2.reload()

    def reverse(self):
        self.edit.reverse()
        self.edit.save(self.img_s)
        self.img2.reload()

    def mirror(self):
        self.edit.mirror()
        self.edit.save(self.img_s)
        self.img2.reload()


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


if __name__ == "__main__":
    MainApp().run()
