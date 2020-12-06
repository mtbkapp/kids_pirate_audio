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
    def __init__(self, playlist):
        self.playlist = playlist
        self.song_idx = 0
        self.restart_player()

    def play_pause(self):
        self.vlc.pause()

    def next(self):
        if (self.song_idx < len(self.playlist) - 1):
            self.song_idx += 1
            self.restart_player()
            print('next song')

    def prev_or_restart(self):
        if self.vlc.get_time() < 1000 and self.song_idx > 0:
            self.song_idx -= 1
            self.restart_player()
            print('prev song')
        else:
            if self.is_playing():
                self.vlc.set_position(0)
            else:
                self.restart_player()

    def volume_up(self):
        self.move_volume(1)

    def volume_down(self):
        self.move_volume(-1)

    def move_volume(self, direction):
        global _volume
        _volume = max(0, min(100, _volume + (direction * 10)))
        self.vlc.audio_set_volume(_volume)
        print('setting volume to %d' % (_volume))

    def restart_player(self):
        print('rebuilding player')
        if hasattr(self, 'vlc'):
            self.dispose()
        self.vlc = vlc.MediaPlayer(self.playlist[self.song_idx])
        self.vlc.play()
        global _volume
        self.vlc.audio_set_volume(_volume)

    def dispose(self):
        self.vlc.release()
        self.vlc = None

    def is_playing(self):
        return self.vlc.is_playing() == 1

    def get_track_info(self):
        total_seconds = int(self.vlc.get_time() / 1000)
        media = self.vlc.get_media()
        media.parse()
        return {'title': media.get_meta(0),
                'album': media.get_meta(4),
                'artist': media.get_meta(1),
                'track': self.song_idx + 1,
                'track_count': len(self.playlist),
                'progress': self.vlc.get_position(),
                'time': (total_seconds // 60, total_seconds % 60)}


class PlayerUI:
    def __init__(self, app, playlist):
        self.app = app
        self.line_height = 30
        self.selected_btn_idx = 2
        self.buttons = ['volume_down', 'prev', 'play_pause', 'next', 'volume_up']
        self.player = Player(playlist)

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
        self.player.dispose()
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
            self.player.play_pause()
        elif btn == 'volume_up':
            self.player.volume_up()
        elif btn == 'volume_down':
            self.player.volume_down()
        elif btn == 'next':
            self.player.next()
        elif btn == 'prev':
            self.player.prev_or_restart()

    def render(self, base):
        draw = ImageDraw.Draw(base)

        # TODO: scrolling text
        #       album art?
        # track info
        text_pad = 2
        pad_side = 5 
        track_info = self.player.get_track_info()
        progress_str = "%d:%02d" % track_info['time'] 
        track = "Track %d / %d" % (track_info['track'], track_info['track_count'])
        draw.text((pad_side, text_pad), track_info['title'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + self.line_height), track_info['album'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 2)), track_info['artist'], font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 3)), track, font=FONT, fill=WHITE)
        draw.text((pad_side, text_pad + (self.line_height * 4)), progress_str, font=FONT, fill=WHITE)

        # progress bar 
        top = 165 
        bar_h = 14 
        bar_pad = 5
        bar_width = int(track_info['progress'] * (WIDTH - (2 * bar_pad)))
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
        if self.player.is_playing():
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
            self.app.push_view(PlayerUI(self.app, [
                '/home/pi/music/06_My_Oh_My.flac',
                '/home/pi/music/01_Familiarity.flac']))

    def render(self, img):
        draw = ImageDraw.Draw(img)
        draw.text((2,2), "Press select", font=FONT)


class App:
    def __init__(self):
        self.views = [BlankView(self), PlayerUI(self, [
                '/home/pi/music/06_My_Oh_My.flac',
                '/home/pi/music/01_Familiarity.flac'])]

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
