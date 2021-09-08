"""
    Settings file.
"""
import pathlib
from typing import Optional


class Config:
    DB_NAME: str = "local.db"
    TG_TOKEN: str = "your_token_tg_bot"
    TG_USERNAME: Optional[str] = "mrgickcool"
    TG_SECRET_PASS: Optional[str] = "secret_pass"
    MEETING_DURATION: str = "1:30"
    USER_NAME: str = "bot record"
    OPEN_ZOOM: str = "/usr/bin/zoom %U"
    # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
    MUTE_KEYS: list = ['altleft', 'a']  # keys to mute in zoom
    FULLSCREEN_KEYS: list = ['altleft', 'f11']  # keys to go fullscreen
    START_CAPTURE_KEYS: list = ['ctrl', '[']
    STOP_CAPTURE_KEYS: list = ['ctrl', ']']
