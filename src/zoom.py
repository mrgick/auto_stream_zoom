"""
    Interaction with the zoom.
"""
from config import Config
from images import IMG_DIR, Buttons, Fields
from db import find_one_nearly_meeting
from utils import logger, now
import pyautogui
import time
import pyscreeze
import time
import subprocess
import os
import signal


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
        position = pyautogui.locateCenterOnScreen(image, confidence=0.8)
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

    for x in range(0, 10):
        if click_on_image(Buttons.JOIN_WITH_COMPUTER_AUDIO):
            break
        time.sleep(10)

    pyautogui.hotkey(*Config.MUTE_KEYS)
    pyautogui.hotkey(*Config.FULLSCREEN_KEYS)

    return True


def status_meeting() -> bool:
    """
        Check if the meeting is ongoing.
    """
    return (find_image(Buttons.STATUS_1)[0]
            or find_image(Buttons.STATUS_2)[0])


def start_meeting(meet_id, meet_pass):
    """
        Starting meeting.
    """
    def run_process(command: str, sleep_seconds: int = 10):
        """
            Start program throw command
        """
        process = subprocess.Popen(command, shell=True)
        time.sleep(sleep_seconds)

    def kill_process(name: str) -> bool:
        """
            Kill process by name.
        """
        try:
            self_pid: int = os.getpid()
            for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
                pid: int = int(line.split()[0])
                if pid != self_pid:
                    os.kill(pid, signal.SIGKILL)
            logger.info("Killed process with name " + name)
            return True
        except Exception as e:
            logger.error("Trying killed " + name + "\n" + str(e))
            return False

    kill_process("zoom")
    run_process(Config.OPEN_ZOOM)
    join_meeting(meet_id, meet_pass)


def start_zoom() -> None:
    while True:
        meeting = None
        try:
            if meeting is None:
                meeting = find_one_nearly_meeting()
            if meeting["status"] is True:
                meet = meeting["query"]
                logger.info("Waiting meeting" + str(meet))
                while now() <= meet[0]:
                    time.sleep(10)
                logger.info("Starting meeting" + str(meet))
                pyautogui.hotkey(*Config.START_CAPTURE_KEYS)
                while now() < meet[1]:
                    if status_meeting() is False:
                        start_meeting(meet[2], meet[3])
                    time.sleep(60)
                logger.info("Ending meeting" + str(meet))
                pyautogui.hotkey(*Config.STOP_CAPTURE_KEYS)
                meeting = None
            else:
                time.sleep(10)
        except Exception as e:
            logger.error(e)
    pyautogui.hotkey(*Config.START_CAPTURE_KEYS)