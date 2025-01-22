from kivy.uix.screenmanager import Screen, ScreenManager
import time
from kivy.graphics.texture import Texture
from ImgTools.Video import Video
import threading
from kivy.clock import Clock
from functools import partial
from kivy.uix.image import Image



class VideoScreen(Screen):
    
    def __init__(self, **kw):
        super(VideoScreen, self).__init__(**kw)
        
        self.frame = None
        self.img_name = None
        self.dir = None
        self.video = None
        self.running = False
               
        # self.cam = Image()
        
    def on_enter(self, *args):
        
        threading.Thread(target=self.start_video, daemon=True).start()                        
        
        return super().on_enter(*args)

    def start_video(self):
        self.video = Video()
        # self.ids.holder.add_widget(self.cam)
                
        self.running = True
        
        while self.running:
            self.video.read_frame()
            self.frame = self.video.frame
            
            Clock.schedule_once(self.display_frame)
            
        self.video.release()
    
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        # self.ids.cam.play = False

    def take(self):
        # self.ids.holder.remove_widget(self.cam)       
        self.video.save_img()
        self.img_name = self.video.img_name
        self.dir = self.video.dir
        self.running = False
        self.manager.current = "photo_screen"
        
    def none_filter(self):
        self.video.no_mask()
        
    def rect_filter(self):
        self.video.plain_mask()
        
    def bat_filter(self):
        self.video.bat_mask()
        
    def flash_filter(self):
        self.video.flash_mask()
        
    def display_frame(self, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(self.frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        # self.ids.cam.texture = texture
        self.ids.cam.texture = texture


