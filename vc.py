from Tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import math

WIDTH = 240
HEIGHT = 240
FONT = ImageFont.truetype('DejaVuSansMono.ttf', 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ViewController
# * accepts input
# * renders itself by returning a full screen PIL image
# * call tell app to rerender at any time

# StackViewController
# * contains a stack of view controllers
# * routes input to the current view controller
# * renders itself by rendering the current view controller
# * exposes a way to push and pop new views controllers to the stack view controller



# ViewController base class. All view controllers should inherit from this
# class and override the draw and handle_input methods
class ViewController:
    def __init__(self, app):
        self.app = app

    def draw(self, draw):
        draw.text((10,10), "no draw impl", font=FONT, fill=WHITE)

    def handle_input(self, label):
        print("got input %s" % (label))

    def rerender(self):
        self.app.render()

    def render(self):
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)
        self.draw(draw)
        return img


class StackedViewController(ViewController):
    def __init__(self, app, vc):
        ViewController.__init__(self, app)
        self.controllers = [vc]


class PlayerViewController(ViewController):
    def __init__(self, app, songs):
        ViewController.__init__(self, app)
        self.songs = songs
        self.song_idx = 0
        self.tile_height = 30
        self.state = 'playing'
        self.buttons = ['prev', 'play', 'pause']
        self.selected_btn = 1 
        # something that will cause a rerender every half second or so for
        # updating the progress
        # scrolling text

    def draw(self, draw):
        s = self.current_song()
        track = "Track %d / %d" % (self.song_idx + 1, len(self.songs))
        progress = "%d:%d" % (2, 30)

        draw.text((2, 2), s['title'], font=FONT, fill=WHITE)
        draw.text((2, 2 + self.tile_height), s['album'], font=FONT, fill=WHITE)
        draw.text((2, 2 + (self.tile_height * 2)), s['artist'], font=FONT, fill=WHITE)
        draw.text((2, 2 + (self.tile_height * 3)), track, font=FONT, fill=WHITE)
        draw.text((2, 2 + (self.tile_height * 4)), progress, font=FONT, fill=WHITE)

        self.draw_prev_btn(draw, self.current_btn() == 'prev')

    def draw_prev_btn(self, draw, is_selected):
        rp(draw, 100, 100, 50, 3, 0)


    def rp(self, draw, cx, cy, radius, sides, rot):
        angle = 2 * math.pi / sides
        points = []
        for s in range(sides):
            a = rot + (angle * s) 
            # find x and y and put into points 
        draw.polygon


    def current_song(self):
        return self.songs[self.song_idx]

    def play_pause(self):
        if self.state == 'playing':
            self.pause()
        else:
            self.play()

    def play(self):
        self.state = 'playing'

    def pause(self):
        self.state = 'paused'

    def next(self):
        self.play()
        self.song_idx = min(len(self.songs) - 1, self.song_idx + 1)

    def prev(self):
        self.play()
        self.song_idx = max(0, self.song_idx - 1)

    def select(self):
        print(self.current_btn)

    def current_btn(self):
        return self.buttons[self.selected_btn]

    def next_btn(self):
        self.selected_btn = (self.selected_btn + 1) % len(self.buttons)

    def prev_btn(self):
        self.selected_btn = (self.selected_btn - 1) % len(self.buttons)



test_songs = [
        {
            'title': 'SOULFUL - Live', 
            'album': 'Chronology Of A Dream: Live At The Village Vanguard',
            'artist': 'Jon Batist'
            }, {
                'title': 'ORDR - Live',
                'album': 'Chronology Of A Dream: Live At The Village Vanguard',
                'artist': 'Jon Batist'
                }
            ]



class App:
    def __init__(self, tk_root):
        self.tk_root = tk_root
        self.tk_root.geometry("500x500")
        self.tk_root.title("Pirate Audio UI Emulator")
        #self.vc = ViewController(self)
        self.vc = PlayerViewController(self, test_songs) 
        self.add_buttons()
        self.render()

    def render(self):
        if hasattr(self, 'display'):
            print("display destroy")
            self.display.destroy()
        tkpi = ImageTk.PhotoImage(self.vc.render())
        self.display = Label(self.tk_root, image=tkpi)
        self.display.image = tkpi
        self.display.place(x=100,y=10, width=WIDTH, height=HEIGHT)

    def add_buttons(self):
        btn_a = Button(self.tk_root, text="A", command=self.push_a)
        btn_a.place(x=10, y=10)
        
        btn_b = Button(self.tk_root, text="B", command=self.push_b)
        btn_b.place(x=10, y=100)

        btn_x = Button(self.tk_root, text="X", command=self.push_x)
        btn_x.place(x=400, y=10)
        
        btn_y = Button(self.tk_root, text="Y", command=self.push_y)
        btn_y.place(x=400, y=100)

    def push_a(self):
        self.send_input("A")

    def push_b(self):
        self.send_input("B")
        
    def push_x(self):
        self.send_input("X")

    def push_y(self):
        self.send_input("Y")

    def send_input(self, label):
        self.vc.handle_input(label)

    def start(self): 
        self.tk_root.mainloop()


App(Tk()).start()
