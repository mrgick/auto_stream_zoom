from config import Config
from zoom import join_meeting, status_meeting
from utils import logger
import time
import subprocess
import os
import signal
from datetime import datetime


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


meeting_id: str = "7019483603"
meeting_pass: str = "4VXMrJ"
meeting_time_start: str = "2021-08-25 21:18"
meeting_time_end: str = "2021-08-25 22:18"


def start_meeting():
    kill_process("zoom")
    run_process(Config.OPEN_ZOOM)
    join_meeting(meeting_id, meeting_pass)


def str_to_datetime(str_time: str) -> datetime:
    """
        Get datetime from string.
    """
    return datetime.fromisoformat(str_time)


def main() -> None:
    start_meeting()
    meeting_time_end = str_to_datetime(meeting_time_end)
    while datetime.now() < meeting_time_end:
        if status_meeting() is False:
            start_meeting()
        time.sleep(60)

    print("done")


if __name__ == "__main__":
    main()
