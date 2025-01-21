from kivy.uix.screenmanager import Screen, ScreenManager
import time
from kivy.graphics.texture import Texture
from ImgTools.Video import Video

class VideoScreen(Screen):
    
    def __init__(self, **kw):
        super(VideoScreen, self).__init__(**kw)
        
        self.frame = None
        self.img_name = None
        self.dir = None
        self.video = None
        
    def on_enter(self, *args):
        self.video = Video()
        
        return super().on_enter(*args)

    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        # self.ids.cam.play = False

    def take(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.dir = "IMGS"
        self.img_name = f"IMG_{timestr}.png"
        self.ids.cam.export_to_png(f"./{self.dir}/{self.img_name}")
        self.manager.current = "photo_screen"
        
    def display_frame(self, frame, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.main_screen.ids.vid.texture = texture


