import functools
from logging import getLogger

from log.config import init_logging
from server.server import Server

# Logging初期化
init_logging()
LOGGER = getLogger()

# https://qiita.com/HidKamiya/items/9e941a5389ba5eb79df1
print = functools.partial(print, flush=True)

if __name__ == "__main__":
    server = Server()
