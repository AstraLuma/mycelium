#!/usr/bin/env python3
import enum
import logging
import time

import board
import neopixel

POTS = 12
PIXELS_PER_POT = 12

logging.basicConfig(
    level='DEBUG',
)


pixels = neopixel.NeoPixel(board.D18, POTS * PIXELS_PER_POT, brightness=0.3, auto_write=False)


class States(enum.Enum):
    BLANK = enum.auto()
    GOOD = enum.auto()
    BAD = enum.auto()
    WEIRD = enum.auto()


COLORS = {
    States.BLANK: (64, 64, 64),
    States.GOOD: (0, 255, 0),
    States.BAD: (255, 0, 0),
    States.WEIRD: (255, 0, 255),
}


def xmas():
    for i in range(len(pixels)):
        pixels[i] = COLORS[States.GOOD if i % 2 else States.BAD]


while True:
    pixels.fill(COLORS[States.BLANK])
    pixels.show()
    time.sleep(1)

    pixels.fill(COLORS[States.GOOD])
    pixels.show()
    time.sleep(1)

    pixels.fill(COLORS[States.BAD])
    pixels.show()
    time.sleep(1)

    pixels.fill(COLORS[States.WEIRD])
    pixels.show()
    time.sleep(1)

    xmas()
    pixels.show()
    time.sleep(1)
