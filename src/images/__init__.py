"""
    Dir with all images.
"""
import pathlib

IMG_DIR = pathlib.Path(__file__).parent.resolve()


class Buttons:
    JOIN_A_MEETING: str = "join_a_meeting.png"
    DO_NOT_CONNECT_TO_AUDIO: str = "do_not_connect_to_audio.png"
    TURN_OFF_MY_VIDEO: str = "turn_off_my_video.png"
    JOIN: str = "join.png"
    JOIN_WITH_COMPUTER_AUDIO: str = "join_with_computer_audio.png"
    STATUS_1: str = "status_1.png"
    STATUS_2: str = "status_2.png"


class Fields:
    ENTER_MEETING_ID: str = "enter_meeting_id.png"
    ENTER_NAME: str = "enter_name.png"
    PASSCODE: str = "passcode.png"
