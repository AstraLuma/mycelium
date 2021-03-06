import socket
import subprocess
import urllib.request

from checklib import check


@check
def ping(host):
    """
    Did the host answer a ping?
    """
    subprocess.run(['ping', '-c', '1', host], check=True, stdout=subprocess.DEVNULL)


@check
def tcp(host, port, timeout=10):
    """
    Can I connect to this port?
    """
    s = socket.create_connection((host, port), timeout=timeout)
    s.close()


@check
def url(address):
    """
    Is this URL available?
    """
    with urllib.request.urlopen(address):
        pass
