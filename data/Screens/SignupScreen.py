import json
from kivy.uix.screenmanager import Screen, ScreenManager
from datetime import datetime


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
