"""
    Settings file.
"""
import pathlib


class Config:
    USER_NAME: str = "bot record"
    OPEN_ZOOM: str = "/usr/bin/zoom %U"
    # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    MUTE_KEYS: str = ['altleft', 'a']  # keys to mute in zoom
    FULLSCREEN_KEYS: str = ['altleft', 'f10']  # keys to go fullscreen
