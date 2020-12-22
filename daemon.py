#!/usr/bin/env python3
import contextlib
import logging
import os
import pathlib
import time

import board
import jinja2
import neopixel
from cysystemd.daemon import notify, Notification
from cysystemd import journal


from checklib import States, load
import checks

PIXELS_PER_POT = 12

__pfile__ = pathlib.Path(__file__).absolute()
ROOT = __pfile__.parent

CONFIG_FILE = ROOT / 'mycelium.yaml'

HTTP_DIR = pathlib.Path('/run/www')

logging.basicConfig(
    level='DEBUG',
    # handlers=[journal.JournaldLogHandler()] if 'JOURNAL_STREAM' in os.environ else None,
)

LOG = logging.getLogger()


COLORS = {
    States.BLANK: (16, 16, 16),
    States.GOOD: (0, 255, 0),
    States.BAD: (255, 0, 0),
    States.WEIRD: (255, 0, 255),
}


@contextlib.contextmanager
def systemd_daemon():
    if 'NOTIFY_SOCKET' in os.environ:
        notify(Notification.READY)
        try:
            yield
        finally:
            notify(Notification.STOPPING)
    else:
        yield


# LOG.debug("environ: %r", os.environ)

with open(CONFIG_FILE) as c:
    config = load(checks, c)

LOG.debug("config: %r", config)

pixels = neopixel.NeoPixel(board.D18, len(config) * PIXELS_PER_POT, brightness=0.3, auto_write=False)

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ROOT / 'templates'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)
html_template = jinja_env.get_template('index.html')

HTTP_DIR.mkdir(parents=True, exist_ok=True)

with systemd_daemon(), pixels:
    pixels.fill(COLORS[States.BLANK])
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

        # Render to HTML
        with open(HTTP_DIR / 'index.html', 'wt') as f:
            f.write(html_template.render(results=results))

        # Sleep
        time.sleep(60)
