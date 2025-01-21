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
from kivy.graphics import Color, Rectangle
from Screens.hoverable import HoverBehavior
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
import time

from ImgTools.ImgDraw import ImgDraw

from Screens.LoginScreen import LoginScreen
from Screens.SignupScreen import SignUpScreen
from Screens.Success import Success
from Screens.PhotoScreen import PhotoScreen
from Screens.VideoScreen import VideoScreen

# Builder.load_file("main.kv")
                              

class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        root = RootWidget()
        root.current = "login_screen"
        print("Current screen:", root.current)  # Debug print
        return root


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

