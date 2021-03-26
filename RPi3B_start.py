# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import digitalio
import board
import sys
import time

from adafruit_rgb_display.rgb import color565
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

def td(y,txt,fill_colour): # draw line of text
    draw.text((x,y),txt,font=font, fill=fill_colour)

# Configuration for CS and DC pins for Raspberry Pi
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # The pi can be very fast!
# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = display.width  # we swap height/width to rotate it to landscape!
width = display.height
image = Image.new("RGB", (width, height))
rotation = 0

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

image = Image.open("/home/pi/pi.jpg")

# scale the image to the smaller screen dimension:
image_ratio = image.width / image.height
screen_ratio = width / height
if screen_ratio < image_ratio:
    scaled_width = image.width * height // image.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = image.height * width // image.width
image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# crop and center the image:
x_jpg = scaled_width // 2 - width // 2
y_jpg = scaled_height // 2 - height // 2
image = image.crop((x_jpg, y_jpg, x_jpg + width, y_jpg + height))

# display image:
display.image(image)
time.sleep(3.0)

# create blank image for drawing with mode 'RGB' for full color:
image = Image.new("RGB", (width, height))
rotation = 0

# get drawing object to draw on image:
draw = ImageDraw.Draw(image)

# draw a black filled box to clear the image:
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
display.image(image, rotation)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# configure colours
WHITE = "#FFFFFF"
GREY = "#7A7A7A"
AMBER = "#fc8106"
GREEN = "#00EE00"
RED = "#FF3030"
BLACK = "#000000"
YELLOW = "#FFFF00"
CYAN = "#FF00FF"

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# define and draw text
L1 = [18, "Press top switch\n 24 to start\n FortiusAnt", YELLOW]
L2 = [131, "Press bottom\n switch 23 to exit", CYAN]
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
td(L1[0], L1[1], L1[2])
td(L2[0], L2[1], L2[2])

# display text
display.image(image, rotation)
    
# Main loop:
while True:

    if buttonA.value and not buttonB.value:  # just button A pressed
        backlight.value = False  # turn off backlight
        sys.stdout.write('startFA')
        sys.exit(0)
    if buttonB.value and not buttonA.value:  # just button B pressed
#        print("stopping prog")
        backlight.value = False  # turn off backlight
        sys.stdout.write('end')
        sys.exit(0)
