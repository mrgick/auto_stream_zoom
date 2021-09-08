from config import Config
from utils import str_to_datetime, add_duration_to_datetime
from db import insert_meeting, get_all_meetings
from telebot import TeleBot, types
from typing import Callable, Union, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bot = TeleBot(Config.TG_TOKEN)
meetings_dict = {}


class Meeting:
    def __init__(self, meet_id):
        self.meet_id: str = meet_id
        self.meet_pass: Optional[str] = None
        self.time_start: Union[datetime, None] = None
        self.time_end: Union[datetime, None] = None


def check_access(
        func: Callable[[], types.Message]) -> Callable[[], types.Message]:
    """
        Checks access.
        Checking username and secret_pass.
    """
    def wrapper(message: types.Message) -> None:
        access = False
        if Config.TG_USERNAME:
            if message.from_user.username == Config.TG_USERNAME:
                access = True
        if Config.TG_SECRET_PASS:
            if Config.TG_SECRET_PASS in message.text:
                access = True

        if access:
            func(message)
        else:
            bot.reply_to(
                message, "No access!\n"
                "Add secret_pass to message or"
                "add your telegram username in config!\n"
                "To see your username type /get_username")

    return wrapper


@bot.message_handler(commands=['get_username'])
def get_username(message: types.Message) -> None:
    """
        Getting Telegram username.
    """
    bot.reply_to(message, message.from_user.username)


@bot.message_handler(commands=['help'])
@check_access
def help_text(message: types.Message) -> None:
    """
        Sending help about the bot.
    """
    bot.reply_to(message, "TODO: need to write help\n /add_meeting")


@bot.message_handler(commands=['add_meeting'])
@check_access
def add_meeting(message: types.Message) -> None:
    """
        Adding meeting func.
    """
    def add_meeting_id(message: types.Message) -> None:
        meet_id = message.text.replace(' ', '')
        if len(meet_id) != 10 or not meet_id.isdigit():
            msg = bot.reply_to(message, 'Meeting id should be 10 numbers.\n')
            bot.register_next_step_handler(msg, add_meeting_id)
        else:
            meetings_dict[message.chat.id] = Meeting(meet_id)
            msg = bot.reply_to(message, 'Write meeting password.')
            bot.register_next_step_handler(msg, add_meeting_pass)

    def add_meeting_pass(message: types.Message) -> None:
        meet_pass = message.text.replace(' ', '')
        meeting = meetings_dict[message.chat.id]
        meeting.meet_pass = meet_pass
        msg = bot.reply_to(message, 'Write meeting start time.\n'
                                    'Example: 2021-08-31 12:53 or 12:53\n'
                                    'For smaller variant add next, '
                                    'if it will be on next day.')
        bot.register_next_step_handler(msg, add_meeting_start_time)

    def add_meeting_start_time(message: types.Message) -> None:
        next_day = False
        if "next" in message.text.lower():
            message.text = message.text.lower().replace('next', '')
            message.text.replace(' ', '')
            next_day = True
        time_start = str_to_datetime(message.text, next_day)
        if time_start is None:
            msg = bot.reply_to(message, 'Wrong time, please write again.')
            bot.register_next_step_handler(msg, add_meeting_start_time)
        else:
            meeting = meetings_dict[message.chat.id]
            meeting.time_start = time_start
            msg = bot.reply_to(message,
                               'Meeting will start at ' + str(time_start) +
                               '\nWrite meeting duration.\n' +
                               'Example: 1:30 \n' +
                               'Or type yes to plus default duration')
            bot.register_next_step_handler(msg, add_meeting_end_time)

    def add_meeting_end_time(message: types.Message) -> None:
        meeting = meetings_dict[message.chat.id]
        if "yes" in message.text.lower():
            duration = Config.MEETING_DURATION

        else:
            duration = message.text.replace(' ', '')
        time_end = add_duration_to_datetime(meeting.time_start, duration)
        if time_end is None:
            msg = bot.reply_to(message, 'Wrong time, please write again.')
            bot.register_next_step_handler(msg, add_meeting_end_time)
        else:
            meeting.time_end = time_end
            inserted = insert_meeting(
                time_start=str(meeting.time_start),
                time_end=str(meeting.time_end),
                meet_id=meeting.meet_id,
                meet_pass=meeting.meet_pass
            )
            if inserted["status"] is False:
                bot.reply_to(message, inserted["msg"])
            else:
                bot.reply_to(message,
                             'Added meeting:\n' + str(inserted["query"]))

    msg = bot.reply_to(message,
                       'Adding new meeting.\n'
                       'Write meeting id.\n'
                       'Example: 1234567890')
    bot.register_next_step_handler(msg, add_meeting_id)


@bot.message_handler(commands=['show_all'])
@check_access
def text(message: types.Message) -> None:
    """
        Sending default text.
    """
    meetings = get_all_meetings()
    if meetings["status"] is False:
        bot.reply_to(message, "Error:\n" + meetings['msg'])
    else:
        msg = meetings['msg'] + "\n"
        msg += ''.join([str(row) + "\n" for row in meetings["query"]])
        bot.reply_to(message, msg)


@bot.message_handler(func=lambda message: True)
@check_access
def text(message: types.Message) -> None:
    """
        Sending default text.
    """
    bot.reply_to(message, "To see help type /help")


def start_tg_bot():
    bot.polling(none_stop=True, interval=0)
