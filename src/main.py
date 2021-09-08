from db import init_db
from zoom import start_zoom
from telegram import start_tg_bot
import threading
import logging

logger = logging.getLogger(__name__)
    

def main() -> None:
    status = init_db()
    if status['status'] is False:
        logger.error(status['msg'])
    threading.Thread(target=start_tg_bot).start()
    threading.Thread(target=start_zoom).start()


if __name__ == "__main__":
    main()
