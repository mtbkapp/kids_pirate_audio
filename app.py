from PIL import Image, ImageDraw, ImageFont
import math
import vlc

WIDTH = 240
HEIGHT = 240
FONT = ImageFont.truetype('DejaVuSansMono.ttf', 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ICON_SIZE = 36
MAX_VOLUME = 100

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

_volume = 50  # so the volume is remembered between Player instances

class Player:
    def __init__(self, app, playlist):
        self.app = app
        self.line_height = 30
        self.selected_btn_idx = 2
        self.buttons = ['volume_down', 'prev', 'play_pause', 'next', 'volume_up']
        self.playing = True
        self.playlist = playlist
        self.playlist_idx = 0
        self.player = vlc.MediaPlayer(playlist[self.playlist_idx])
        self.player.play()
        self.player.audio_set_volume(_volume)

    def handle_input(self, label):
        if label == 'A':
            self.sel_prev_btn()
        elif label == 'B':
            self.sel_next_btn()
        elif label == 'Y':
            self.push_btn()
        elif label == 'X':
            self.exit()

    def exit(self):
        p = self.player
        self.player = None
        p.release()
        self.app.pop_view()

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
        elif btn == 'volume_up':
            self.vol_up()
        elif btn == 'volume_down':
            self.vol_down()

    def vol_up(self):
        _volume = min(MAX_VOLUME, _volume + 10)
        self.player.audio_set_volume(_volume)
        print("set volume to %d" % _volume)

    def vol_down(self):
        _volume = max(0, _volume - 10)
        self.player.audio_set_volume(_volume)
        print("set volume to %d" % _volume)

    def toggle_play_pause(self):
        self.playing = not self.playing
        self.player.pause()
        print("toggle play pause to %s" % self.playing)

    def render(self, base):
        draw = ImageDraw.Draw(base)

        # track info
        text_pad = 2
        pad_side = 5 
        track = "Track %d / %d" % (5, 13)

        progress_seconds = int(self.player.get_time() / 1000)
        progress = (math.floor(progress_seconds / 60), progress_seconds % 60)
        progress_str = "%d:%02d" % progress 
        s = {'title': 'Long Descriptive Title', 'album': 'Arbol de Luz', 'artist': 'watman'}
        draw.text((pad_side, text_pad), s['title'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + self.line_height), s['album'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 2)), s['artist'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 3)), track, font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 4)), progress_str, font=FONT, fill=WHITE)

        # progress bar 
        top = 165 
        bar_h = 14 
        bar_pad = 5
        bar_width = int(self.player.get_position() * (WIDTH - (2 * bar_pad)))
        print(bar_width)
        draw.rectangle([(bar_pad, top), ((WIDTH - bar_pad), top + bar_h)], fill=BLACK, outline=WHITE, width=2)
        draw.rectangle([(bar_pad, top), (bar_width + bar_pad, top + bar_h)], fill=WHITE)

        # virtual buttons
        h = HEIGHT - ICON_SIZE - 10
        p0 = (2, h)
        p1 = (52, h)
        p2 = (102, h)
        p3 = (152, h)
        p4 = (202, h)

        self.render_btn(base, 'volume_down', IMG_VOL_DOWN, IMG_VOL_DOWN_SELECTED, p0)
        self.render_btn(base, 'prev', IMG_PREV, IMG_PREV_SELECTED, p1)
        if self.playing:
            self.render_btn(base, 'play_pause', IMG_PAUSE, IMG_PAUSE_SELECTED, p2)
        else:
            self.render_btn(base, 'play_pause', IMG_PLAY, IMG_PLAY_SELECTED, p2)
        self.render_btn(base, 'next', IMG_NEXT, IMG_NEXT_SELECTED, p3)
        self.render_btn(base, 'volume_up', IMG_VOL_UP, IMG_VOL_UP_SELECTED, p4)

    def render_btn(self, base, name, img, img_selected, pos):
        base.paste(img_selected if self.current_btn() == name else img, pos)


class BlankView:
    def __init__(self, app):
        self.app = app

    def handle_input(self, label):
        if label == 'Y':
            self.app.push_view(Player(self.app, ['/home/mtbkapp/Downloads/06_My_Oh_My.flac']))

    def render(self, img):
        draw = ImageDraw.Draw(img)
        draw.text((2,2), "Press select", font=FONT)


class App:
    def __init__(self):
        self.views = [BlankView(self), Player(self, ['/home/mtbkapp/Downloads/06_My_Oh_My.flac'])]

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
