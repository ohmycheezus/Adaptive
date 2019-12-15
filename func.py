import ctypes
import time


SPI_GETDESKWALLPAPER = 0x0073
SPI_SETDESKWALLPAPER = 20
ubuf = ctypes.create_unicode_buffer(200)


def getdefault():
    if ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, 200, ubuf, 0):
        default_wp = ubuf.value
        return default_wp


def setdeskwallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, path, 0)


def setdefault(getdefault):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, getdefault, 0)
    