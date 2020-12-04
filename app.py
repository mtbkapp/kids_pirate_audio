from PIL import Image, ImageDraw, ImageFont

WIDTH = 240
HEIGHT = 240
FONT = ImageFont.truetype('DejaVuSansMono.ttf', 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ICON_SIZE = 36

IMG_VOL_UP = Image.open('./icons/arrow-up.png')
IMG_VOL_UP_SELECTED = Image.open('./icons/arrow-up-circle.png')
IMG_VOL_DOWN = Image.open('./icons/arrow-down.png')
IMG_VOL_DOWN_SELECTED = Image.open('./icons/arrow-down-circle.png')
IMG_VOL = Image.open('./icons/volume-2.png')

IMG_PLAY = Image.open('./icons/play.png')
IMG_PLAY_SELECTED = Image.open('./icons/play-circle.png')
IMG_PAUSE = Image.open('./icons/pause.png')
IMG_PAUSE_SELECTED = Image.open('./icons/pause-circle.png')
IMG_NEXT = Image.open('./icons/arrow-right.png')
IMG_NEXT_SELECTED = Image.open('./icons/arrow-right-circle.png')
IMG_PREV = Image.open('./icons/arrow-left.png')
IMG_PREV_SELECTED = Image.open('./icons/arrow-left-circle.png')

class Player:
    def __init__(self, app):
        self.app = app
        self.line_height = 30
        self.selected_btn_idx = 2
        self.buttons = ['volume_down', 'prev', 'play_pause', 'next', 'volume_up']
        self.playing = True
        self.volume = 50

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
        top = 150 
        draw.rectangle([(pad_side, top), (WIDTH - pad_side, top + h)], fill=WHITE)

        h = HEIGHT - 10 - ICON_SIZE 
        p0 = (2, h)
        p1 = (52, h)
        p2 = (102, h)
        p3 = (152, h)
        p4 = (202, h)

        self.render_btn(base, 'volume_down', IMG_VOL_UP, IMG_VOL_UP_SELECTED, p0)
        self.render_btn(base, 'prev', IMG_PREV, IMG_PREV_SELECTED, p1)
        if self.playing:
            self.render_btn(base, 'play_pause', IMG_PAUSE, IMG_PAUSE_SELECTED, p2)
        else:
            self.render_btn(base, 'play_pause', IMG_PLAY, IMG_PLAY_SELECTED, p2)
        self.render_btn(base, 'next', IMG_NEXT, IMG_NEXT_SELECTED, p3)
        self.render_btn(base, 'volume_up', IMG_VOL_DOWN, IMG_VOL_DOWN_SELECTED, p4)

    def render_btn(self, base, name, img, img_selected, pos):
        base.paste(img_selected if self.current_btn() == name else img, pos)


        



class BlankView:
    def __init__(self, app):
        self.app = app

    def handle_input(self, label):
        if label == 'Y':
            self.app.push_view(Player(self.app))

    def render(self, img):
        draw = ImageDraw.Draw(img)
        draw.text((2,2), "Press select", font=FONT)


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
