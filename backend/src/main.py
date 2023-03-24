import functools
import sys
from logging import getLogger

from command.processor import CommandProcessor
from config import Config
from db import manager
from log.config import init_logging
from socket_lib.server import Server
from util.log import error_trace

# https://qiita.com/HidKamiya/items/9e941a5389ba5eb79df1
print = functools.partial(print, flush=True)
LOGGER = getLogger(__name__)


def init():
    # Logging初期化
    init_logging()

    # マスターテーブルセットアップ
    manager.setup()

    Config.FRONTEND_SERVER_PORT = int(sys.argv[1])


if __name__ == "__main__":
    try:
        init()

        LOGGER.info("[Server] Start")

        server = Server()
        server.start(Config.FRONTEND_SERVER_PORT, CommandProcessor())

        LOGGER.info("[Server] End")
    except Exception as e:
        error_trace(e)
