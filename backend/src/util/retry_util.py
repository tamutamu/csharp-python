from logging import getLogger
from time import sleep

from config import Config, Const
from socket_lib.client import LocalClient
from util.log import error_trace

LOGGER = getLogger(__name__)
client = LocalClient()


def func_with_retry(func, max_retry=10, await_time=5):
    retry = 0

    while True:
        try:
            return func()
        except Exception as e:
            error_trace(e)
            retry += 1

            if max_retry >= retry:
                LOGGER.error(f"再試行を行います [{retry}回目]")
                sleep(await_time)
            else:
                LOGGER.error("処理失敗")
                client.send({"status": Const.Status.EXIT, "result": Const.Result.FAILED}, Config.FRONTEND_SERVER_PORT)
