# kids\_pirate\_audio

## Dev Setup (Ubuntu 20.10)
* Install apt packages `sudo apt update && sudo apt install python3 python3-venv python3-pip`
* Setup virtual environment `python3 -m venv .venv`
* Activate virtual environment  `source .venv/bin/activate`
* Install pip packages `pip install pillow python-vlc`
* Start app `python emulator.py`

## Raspberry PI OS 
* No virtual env
* Install package packages `sudo apt update && sudo apt install python3-rpi.gpio python3-spidev python3-pip python3-pil python3-numpy vlc python3-vlc`
* Start app `python3 pi.py`

## VLC Python Binding Docs
https://www.olivieraubert.net/vlc/python-ctypes/doc/

## Pirate Audio Hardware Docs
https://github.com/pimoroni/pirate-audio
https://github.com/pimoroni/st7789-python


## Disclaimers
* I'm a beginner python / Raspberry PI programmer
* Only tested on Raaspberry Pi 2 and dev setup with Ubuntu Mate 20.10


