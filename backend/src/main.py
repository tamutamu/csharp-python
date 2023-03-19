import functools
import sys
from logging import getLogger

from command.executer import CommandHandler
from db import manager
from log.config import init_logging
from server.server import Server
from util.log import error_trace

# https://qiita.com/HidKamiya/items/9e941a5389ba5eb79df1
print = functools.partial(print, flush=True)
LOGGER = getLogger(__name__)


def init():
    # Logging初期化
    init_logging()

    # マスターテーブルセットアップ
    manager.setup()


if __name__ == "__main__":
    try:
        init()

        LOGGER.info("[Server] Start")

        server = Server()
        port = int(sys.argv[1])
        server.start(port, CommandHandler())

        LOGGER.info("[Server] End")
    except Exception as e:
        error_trace(e)
