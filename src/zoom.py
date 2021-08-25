"""
    Interaction with the zoom.
"""
from config import Config
from images import IMG_DIR, Buttons, Fields
from utils import logger
import pyautogui
import time
import pyscreeze


def write(msg: str, sleep_seconds: int = 1) -> bool:
    """
        Writing message.
    """
    pyautogui.write(msg)
    time.sleep(sleep_seconds)


def find_image(image: str) -> tuple[bool, pyscreeze.Point]:
    """
        Find center position of image on screen.
    """
    image: str = str(IMG_DIR.joinpath(image))
    try:
        position = pyautogui.locateCenterOnScreen(image)
        if not position:
            return False, pyscreeze.Point(0, 0)
        return True, position
    except Exception as e:
        return False, pyscreeze.Point(0, 0)


def click_on_image(image: str, sleep_seconds: int = 2) -> bool:
    """
        Finding image and click on it.
    """
    status, position = find_image(image)
    if status is False:
        return False
    pyautogui.moveTo(position)
    pyautogui.click()
    time.sleep(sleep_seconds)
    return True


def join_meeting(meeting_id: str, meeting_pass: str = "") -> bool:
    """
        Join in the meeting.
        Pressing buttons and writing info in fields.
    """
    if not click_on_image(Buttons.JOIN_A_MEETING):
        logger.error("No window zoom")
        return False

    if not click_on_image(Fields.ENTER_MEETING_ID):
        logger.error("No field for meeting id")
        return False
    write(meeting_id)

    click_on_image(Buttons.DO_NOT_CONNECT_TO_AUDIO)
    click_on_image(Buttons.TURN_OFF_MY_VIDEO)

    if click_on_image(Fields.ENTER_NAME):
        write(Config.USER_NAME)

    click_on_image(Buttons.JOIN, 10)

    if click_on_image(Fields.PASSCODE):
        if meeting_pass == "":
            logger.ERORR("No meeting pass")
            return False
        write(meeting_pass)
        click_on_image(Buttons.JOIN)

    connected: bool = False
    while not connected:
        if click_on_image(Buttons.JOIN_WITH_COMPUTER_AUDIO):
            connected = True
        time.sleep(5)

    pyautogui.hotkey(*Config.MUTE_KEYS)
    pyautogui.hotkey(*Config.FULLSCREEN_KEYS)

    return True


def status_meeting() -> bool:
    """
        Check if the meeting is ongoing.
    """
    return (find_image(Buttons.STATUS_1)[0]
            or find_image(Buttons.STATUS_2)[0])
