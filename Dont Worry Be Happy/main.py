from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
# from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from hoverable import HoverBehavior
import json
from datetime import datetime
from pathlib import Path
import glob
import random
import img
from kivy.graphics.texture import Texture


Builder.load_file("design.kv")


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_in(self, username, password):
        with open("users.json", "r") as file:
            users = json.load(file)
        if username in users and users[username]["password"] == password:
            self.manager.current = "main_screen"
        else:
            self.ids.wrong.text = "Wrong username pr password!"


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
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.gray()

    def log_in(self):
        self.manager.current = "login_screen"

    def gray(self):

        video1 = img.Video(512, 512, 0)


class MainScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()

        available_feelings = glob.glob("quotes/*.txt")
        available_feelings = [Path(i).stem for i in available_feelings]

        if feel in available_feelings:

            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quote = file.readlines()
                print(quote)
            self.ids.tip.text = random.choice(quote)
        else:
            self.ids.tip.text = "This feeling is not in our database"


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class Imagee(ButtonBehavior, Image):
    pass


if __name__ == "__main__":
    MainApp().run()
