import json
from logging import getLogger
from time import sleep

from config import Config, Const
from model.models import SendResponse
from socket_lib.client import LocalClient
from util.json_util import CustomJsonEncoder
from util.log_util import error_trace

LOGGER = getLogger(__name__)
client = LocalClient(Config.FRONTEND_SERVER_PORT)


def func_with_retry(func, max_retry=Config.MAX_RETRY, await_time=5):
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
                response = SendResponse(Const.Status.EXIT, Const.Result.FAILED)
                client.send(response, Config.FRONTEND_SERVER_PORT)

                return json.dumps(response, cls=CustomJsonEncoder)


def func_if_except(bind_func):
    try:
        return bind_func()
    except Exception as e:
        return None


def func_bool_if_except(bind_func):
    try:
        ret = bind_func()
        return (True, ret)
    except Exception as e:
        return (False, e)
