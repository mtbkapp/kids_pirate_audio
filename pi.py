import time
import app
import ST7789
import RPi.GPIO as GPIO

app = app.App()

BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'X', 'Y']
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    app.handle_input(label)

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=100)

disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=13,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000
)

while True:
    disp.display(app.render())
    time.sleep(0.5)

