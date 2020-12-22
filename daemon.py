#!/usr/bin/env python3
import logging
import pathlib
import time

import board
import neopixel

from checklib import States, load
import checks

POTS = 12
PIXELS_PER_POT = 12

__pfile__ = pathlib.Path(__file__).absolute()

CONFIG_FILE = __pfile__.parent / 'mycelium.yaml'

logging.basicConfig(
    level='DEBUG',
)


pixels = neopixel.NeoPixel(board.D18, POTS * PIXELS_PER_POT, brightness=0.3, auto_write=False)


COLORS = {
    States.BLANK: (64, 64, 64),
    States.GOOD: (0, 255, 0),
    States.BAD: (255, 0, 0),
    States.WEIRD: (255, 0, 255),
}


def xmas():
    for i in range(len(pixels)):
        pixels[i] = COLORS[States.GOOD if i % 2 else States.BAD]


with open(CONFIG_FILE) as c:
    config = load(checks, c)

print(config)

while True:
    pixels.fill(COLORS[States.BLANK])
    for i, check in enumerate((c for cs in config.values() for c in cs.values())):
        pixels[i] = COLORS[check()]
    pixels.show()
    time.sleep(1)
