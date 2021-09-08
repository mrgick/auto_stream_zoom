from config import Config
from utils import str_to_datetime, now
import sqlite3
from typing import TypedDict, Callable, Optional
import logging

logger = logging.getLogger(__name__)


class Status(TypedDict):
    status: bool
    msg: str
    query: Optional[tuple]


def error_wrapper(func: Callable) -> Status:
    def wrapper(*args, **kwargs) -> Status:
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(e)
            return {"status": False, "msg": e, "query": None}
    return wrapper


@error_wrapper
def init_db() -> Status:
    """
        Initializing db.
    """
    with sqlite3.connect(Config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT count(name) FROM sqlite_master " +
                    "WHERE type='table' AND name='meetings'")
        if cur.fetchone()[0] != 1:
            cur.execute(''' CREATE TABLE meetings
                            (time_start text,
                            time_end text,
                            id text,
                            pass text) ''')
        con.commit()
        return {"status": True, "msg": "ok", "query": None}


@error_wrapper
def insert_meeting(time_start: str, time_end: str, meet_id: str,
                   meet_pass: str) -> Status:
    """
        Inseting meeting in db.
    """
    with sqlite3.connect(Config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute("select * from meetings where time_start='" +
                    time_start + "'")
        check = cur.fetchone()
        if check is None:
            sql = ''' INSERT INTO meetings(time_start,time_end,id,pass)
                      VALUES(?,?,?,?) '''
            meeting = (time_start, time_end, meet_id, meet_pass)
            cur.execute(sql, meeting)
            con.commit()
            return {
                "status": True,
                "msg": "Added.",
                "query": meeting}
        else:
            return {
                "status": False,
                "msg": "This time start is in bd already.",
                "query": check
            }


@error_wrapper
def delete_meeting(time_start: str) -> Status:
    """
        Inseting meeting in db.
    """
    with sqlite3.connect(Config.DB_NAME) as con:
        cur = con.cursor()
        cur.execute("select * from meetings where time_start='" +
                    time_start + "'")
        check = cur.fetchone()
        if check is None:
            return {
                "status": True,
                "msg": "It wasn't in db.",
                "query": check
            }
        else:
            cur.execute("DELETE FROM meetings where time_start='" +
                        time_start + "'")
            con.commit()
            return {
                "status": True,
                "msg": "Deleted.",
                "query": check}


@error_wrapper
def get_all_meetings() -> Status:
    """
        Get all meetings.
    """
    with sqlite3.connect(Config.DB_NAME) as con:
        cur = con.cursor()
        rows = cur.execute('SELECT * FROM meetings ORDER BY time_start')
    return {
        "status": True,
        "msg": "(time_start, time_end, id, pass)",
        "query": tuple(rows)
    }


@error_wrapper
def find_one_nearly_meeting() -> Status:
    """
        Find one meeting in database with sorted time_start.
    """
    result = get_all_meetings()
    if (result["status"] is False or result["query"] is None
            or result["query"] == ()):
        return {
            "status": False,
            "msg": "Not found.",
            "query": None
        }
    meetings = {}
    for row in result["query"]:
        date = str_to_datetime(row[0])
        if date is not None:
            meetings.update({date: row})
    sorted(meetings.items(), key=lambda p: p[0])
    date_now = now()
    query = None
    for date, value in meetings.items():
        if date_now <= date:
            query = (
                date,
                str_to_datetime(value[1]),
                value[2],
                value[3]
            )
            break
        else:
            delete_meeting(value[0])
    if query:
        return {
            "status": True,
            "msg": "Found.",
            "query": query
        }
    else:
        return {
            "status": False,
            "msg": "DB empty.",
            "query": None
        }


if __name__ == "__main__":
    insert_meeting('2021-08-31 14:59:00', '2021-08-31 12:53:00', '13', '132')
    print(get_all_meetings())
    a = find_one_nearly_meeting()
    print(a)
    # print(delete_meeting('2021-08-31 12:55:00'))
    print(get_all_meetings())
