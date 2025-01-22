import os

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button

from ImgTools.ImgDraw import ImgDraw


class PhotoScreen(Screen):

    def __init__(self, **kw):
        super(PhotoScreen, self).__init__(**kw)
        self.img = Image()
        self.img.size_hint = (1, 1)
        self.add_widget(self.img)
        
    def on_pre_enter(self, *args):
        self.img_name = self.manager.get_screen('video_screen').img_name        
        self.dir = self.manager.get_screen('video_screen').dir
        
        self.edit = ImgDraw(self.img_name, dir=self.dir)

        self.img.source = f"./{self.dir}/{self.img_name}"

        self.img.reload()
        return super().on_pre_enter(*args)
    
    def on_leave(self, *args):
        return super().on_leave(*args)

    def cancel(self):
        self.manager.current = "video_screen"
        os.remove(f"./{self.dir}/{self.img_name}")

    def save(self):
        self.edit.save()
        self.manager.current = "video_screen"

    def reset(self):
        self.edit.reset()
        self.edit.save()
        self.img.reload()

    def one(self):
        self.edit.reset()
        self.edit.draw()
        self.edit.save()
        self.img.reload()

    def two(self):
        self.edit.reset()
        self.edit.fun()
        self.edit.save()
        self.img.reload()

    def three(self):
        self.edit.reset()
        self.edit.gray()
        self.edit.save()
        self.img.reload()

    def reverse(self):
        self.edit.reverse()
        self.edit.save()
        self.img.reload()

    def mirror(self):
        self.edit.mirror()
        self.edit.save()        
        self.img.reload()
        
