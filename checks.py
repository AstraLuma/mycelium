import subprocess

from checklib import check


@check
def ping(host):
    subprocess.run(['ping', '-c', '1', host], check=True, stdout=subprocess.DEVNULL)
