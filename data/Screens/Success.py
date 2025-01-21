from kivy.uix.screenmanager import Screen, ScreenManager


class Success(Screen):

    def log_in(self):
        self.manager.current = "login_screen"