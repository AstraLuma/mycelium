#!/usr/bin/env python3
import logging
import os
import pathlib
import time

import board
import neopixel

from checklib import States, load
import checks

PIXELS_PER_POT = 12

__pfile__ = pathlib.Path(__file__).absolute()

CONFIG_FILE = __pfile__.parent / 'mycelium.yaml'

logging.basicConfig(
    level='DEBUG',
)

LOG = logging.getLogger()


COLORS = {
    States.BLANK: (16, 16, 16),
    States.GOOD: (0, 255, 0),
    States.BAD: (255, 0, 0),
    States.WEIRD: (255, 0, 255),
}

LOG.debug("environ: %r", os.environ)

with open(CONFIG_FILE) as c:
    config = load(checks, c)

LOG.debug("config: %r", config)

pixels = neopixel.NeoPixel(board.D18, len(config) * PIXELS_PER_POT, brightness=0.3, auto_write=False)

while True:
    # Run tests
    results = {
        hostname: {
            checkname: checkfunc()
            for checkname, checkfunc in hostchecks.items()
        }
        for hostname, hostchecks in config.items()
    }

    # Show on LEDs
    pixels.fill(COLORS[States.BLANK])
    for i, res in enumerate((c for cs in results.values() for c in cs.values())):
        pixels[i] = COLORS[res]
    pixels.show()

    # Sleep
    time.sleep(60)
