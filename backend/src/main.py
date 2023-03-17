import functools
import sys
from logging import getLogger

from command.executer import CommandHandler
from db import db
from log.config import init_logging
from server.server import Server

# https://qiita.com/HidKamiya/items/9e941a5389ba5eb79df1
print = functools.partial(print, flush=True)


def init():
    # Logging初期化
    init_logging()

    # マスターテーブルセットアップ
    db.setup()


if __name__ == "__main__":
    init()

    LOGGER = getLogger()
    LOGGER.info("[Server] Start")

    server = Server()
    port = int(sys.argv[1])
    server.start(port, CommandHandler())

    LOGGER.info("[Server] End")
