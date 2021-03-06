from Tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk

WIDTH = 240
HEIGHT = 240
FONT = ImageFont.truetype('DejaVuSansMono.ttf', 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class View:
    def render(self):
        img = Image.new('RGB', (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)
        self.draw(draw)
        return img

class ListView(View):
    def __init__(self, items):
        self.items = items
        self.selected = 0 
        self.display_items = 10
        self.tile_height = HEIGHT / self.display_items
        self.offset = 0
        self.text_pad = 2

    def draw(self, draw):
        tile_idx = 0

        for item_idx in range(self.offset, min(len(self.items), self.offset + self.display_items)):
            text_color = WHITE 
            item = self.items[item_idx]
            if item_idx == self.selected:
                text_color = BLACK 
                x = 0
                y = self.tile_height * tile_idx 
                w = WIDTH - 1
                h = self.tile_height
                rect = (x, y, x + w, y + h)
                draw.rectangle(rect, fill=WHITE)
            draw.text((self.text_pad, (self.tile_height * tile_idx) + self.text_pad), item, font=FONT, fill=text_color)
            tile_idx += 1

    def move_up(self):
        self.selected = max(0, self.selected - 1)
        if self.selected < self.offset:
            self.offset -= 1

    def move_down(self):
        self.selected = min(len(self.items) - 1, self.selected + 1)
        if self.selected > self.offset + self.display_items - 1:
            self.offset += 1

    def get_selected(self):
        return self.items[self.selected]

nested_views = {
        "root": ["bikes", "computers"],
        "bikes": [
            "Trek",
            "GT",
            "Scott CR1",
            "Rocky Mountain Altitude",
            "Torker",
            "Surly Cross Check",
            "Surly Wednesday",
            "Surly Karate Monkey"
            ],
        "computers": [
            "Packard Bell 50mhz",
            "Packard Bell 75mhz",
            "Compaq",
            "White Macbook",
            "Macbook Pro"
            ]
        }

class State:
    def __init__(self):
        self.state = True
        self.view_stack = []
        v = ListView(nested_views['root'])
        self.view_stack.append(v)

    def push_a(self):
        self.current_view().move_up()

    def push_b(self):
        self.current_view().move_down()

    def push_x(self):
        if len(self.view_stack) > 1:
            self.view_stack.pop()

    def push_y(self):
        selected = self.current_view().get_selected()
        if selected in nested_views:
            self.view_stack.append(ListView(nested_views[selected]))

    def current_view(self):
        return self.view_stack[len(self.view_stack) - 1]

    def render(self):
        return self.current_view().render() 


class Emulator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")
        self.root.title("Pirate Audio UI Emulator")
        self.state = State()
        self.name = "Emu"

        self.renderDisplay()

        btn_a = Button(root, text="A", command=self.push_a)
        btn_a.place(x=10, y=10)
        
        btn_b = Button(root, text="B", command=self.push_b)
        btn_b.place(x=10, y=100)

        btn_x = Button(root, text="X", command=self.push_x)
        btn_x.place(x=400, y=10)
        
        btn_y = Button(root, text="Y", command=self.push_y)
        btn_y.place(x=400, y=100)

    def renderDisplay(self):
        if hasattr(self, 'display'):
            self.display.destroy()
        tkpi = ImageTk.PhotoImage(self.state.render())
        self.display = Label(self.root, image=tkpi)
        self.display.image = tkpi
        self.display.place(x=100,y=10, width=WIDTH, height=HEIGHT)

    def push_a(self):
        self.state.push_a()
        self.renderDisplay()

    def push_b(self):
        self.state.push_b()
        self.renderDisplay()

    def push_x(self):
        self.state.push_x()
        self.renderDisplay()

    def push_y(self):
        self.state.push_y()
        self.renderDisplay()

    def start(self): 
        self.root.mainloop()


Emulator(Tk()).start()
