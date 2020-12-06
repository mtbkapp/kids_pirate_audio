from Tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk

WIDTH = 240
HEIGHT = 240
FONT = ImageFont.truetype('DejaVuSansMono.ttf', 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# stack based navigation works well, like iOS's NavigationViewController, nice
#   to keep the state on the stack so on pop returns to the exact scroll state
#   and selection
# don't need any optimizations around when to render
# need to render more often to get song progress to render, and to scroll text
# can't only have access to ImageDraw object because Image.paste is needed for icons
# going back from player view results in music stopping to avoid having to make
#   make a way to go back


# new design:
#  Driver renders app every 1/2 second or so
#  Driver hands input to app then rerenders

ICON_SIZE = 36

class Player:
    def __init__(self, app):
        self.app = app
        self.line_height = 30
        self.play_img = Image.open('./icons/play.png')
        self.play_selected_img = Image.open('./icons/play-circle.png')
        self.pause_img = Image.open('./icons/pause.png')
        self.pause_selected_img = Image.open('./icons/pause-circle.png')
        self.next_img = Image.open('./icons/arrow-right.png')
        self.next_selected_img = Image.open('./icons/arrow-right-circle.png')
        self.prev_img = Image.open('./icons/arrow-left.png')
        self.prev_selected_img = Image.open('./icons/arrow-left-circle.png')
        self.selected_btn_idx = 1
        self.buttons = ['prev', 'play_pause', 'next']
        self.playing = True

    def handle_input(self, label):
        if label == 'A':
            self.sel_prev_btn()
        elif label == 'B':
            self.sel_next_btn()
        elif label == 'Y':
            self.push_btn()
        elif label == 'X':
            self.kill_player()
            self.app.pop_view()

    def kill_player(self):
        print("kill player")


    def current_btn(self):
        return self.buttons[self.selected_btn_idx]

    def sel_next_btn(self):
        self.selected_btn_idx = (self.selected_btn_idx + 1) % len(self.buttons)

    def sel_prev_btn(self):
        self.selected_btn_idx = (self.selected_btn_idx - 1) % len(self.buttons)

    def push_btn(self):
        btn = self.current_btn()
        if btn == 'play_pause':
            self.toggle_play_pause()

    def toggle_play_pause(self):
        self.playing = not self.playing

    def render(self, base):
        draw = ImageDraw.Draw(base)
        pad_side = 5 

        # track info
        text_pad = 2
        track = "Track %d / %d" % (5, 13)
        progress = "%d:%d" % (2, 30)
        s = {'title': 'Long Descriptive Title', 'album': 'Arbol de Luz', 'artist': 'watman'}
        draw.text((pad_side, text_pad), s['title'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + self.line_height), s['album'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 2)), s['artist'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 3)), track, font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 4)), progress, font=FONT, fill=WHITE)

        # progress bar 
        h = 10
        top = 165 
        draw.rectangle([(pad_side, top), (WIDTH - pad_side, top + h)], fill=WHITE)

        # control buttons
        pad_bottom = 10
        h = HEIGHT - ICON_SIZE - pad_bottom
        sel_btn = self.current_btn()

        prev_img = self.prev_selected_img if sel_btn == 'prev' else self.prev_img
        base.paste(prev_img, (pad_side, h))

        play_pause_img = None
        if self.playing:
            play_pause_img = self.pause_selected_img if sel_btn == 'play_pause' else self.pause_img
        else:
            play_pause_img = self.play_selected_img if sel_btn == 'play_pause' else self.play_img
        base.paste(play_pause_img, ((WIDTH / 2) - (ICON_SIZE / 2), h))

        next_img = self.next_selected_img if sel_btn == 'next' else self.next_img
        base.paste(next_img, (WIDTH - ICON_SIZE - pad_side, h))

class BlankView:
    def __init__(self, app):
        self.app = app

    def handle_input(self, label):
        if label == 'Y':
            self.app.push_view(Player(self.app))

    def render(self, img):
        draw = ImageDraw.Draw(img)
        draw.text((2,2), "Press select", font=FONT)


# App's job is to provide interface that the Driver (emulator / real driver)
# expects and to coordinate app level state 
class App:
    def __init__(self):
        self.views = [BlankView(self), Player(self)]

    def handle_input(self, label):
        self.curr_view().handle_input(label)

    def push_view(self, view):
        self.views.append(view)

    def pop_view(self):
        self.views.pop()

    def curr_view(self):
        return self.views[len(self.views) - 1]

    def render(self):
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        self.curr_view().render(img)
        return img




# Emulator Driver class to exchanged for code that interfaces with real 
# Pirate Audio / Raspberry Pi Hardware
class Emulator:
    def __init__(self, tk_root, render_timeout):
        self.tk_root = tk_root
        self.tk_root.geometry("500x500")
        self.tk_root.title("Pirate Audio UI Emulator")
        self.render_timeout = render_timeout
        self.app = App()
        self.add_buttons()
        self.render_loop()

    def render_loop(self):
        self.render()
        self.tk_root.after(self.render_timeout, self.render_loop)

    def render(self):
        if hasattr(self, 'display'):
            self.display.destroy()
        tkpi = ImageTk.PhotoImage(self.app.render())
        self.display = Label(self.tk_root, image=tkpi)
        self.display.image = tkpi
        self.display.place(x=100,y=10, width=WIDTH, height=HEIGHT)

    def add_buttons(self):
        btn_a = Button(self.tk_root, text="A, up", command=self.push_a)
        btn_a.place(x=10, y=10)
        
        btn_b = Button(self.tk_root, text="B, down", command=self.push_b)
        btn_b.place(x=10, y=100)

        btn_x = Button(self.tk_root, text="X, back", command=self.push_x)
        btn_x.place(x=400, y=10)
        
        btn_y = Button(self.tk_root, text="Y, select", command=self.push_y)
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
        self.app.handle_input(label)
        self.render()

    def start(self): 
        self.tk_root.mainloop()


Emulator(Tk(), 500).start()
