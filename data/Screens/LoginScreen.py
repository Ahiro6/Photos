from kivy.uix.screenmanager import Screen, ScreenManager
import json

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
    
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def log_in(self, username, password):
        with open("users.json", "r") as file:
            users = json.load(file)
        if username in users and users[username]["password"] == password:
            self.manager.current = "video_screen"
        else:
            self.ids.wrong.text = "Wrong username or password!"