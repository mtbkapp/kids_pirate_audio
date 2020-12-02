from tkinter import Tk, Button, Label
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys

HEIGHT=240
WIDTH=240
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Emulator:
    def __init__(self, tk_root, app, render_timeout):
        self.tk_root = tk_root
        self.tk_root.geometry("500x500")
        self.tk_root.title("Pirate Audio UI Emulator")
        self.render_timeout = render_timeout
        self.app = app 
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



class TestApp:
    def handle_input(self, label):
        print("input %s" % label)

    def render(self):
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('DejaVuSansMono.ttf', 20)
        draw.text((2,2), "Hello world!", font=font, fill=WHITE)
        return img


if __name__ == '__main__':
    print("Python", sys.version)
    Emulator(Tk(), TestApp(), 500).start()
