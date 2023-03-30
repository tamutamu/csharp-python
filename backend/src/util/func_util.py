import json
from logging import getLogger
from time import sleep

from config import Config, Const
from model.models import SendResponse
from socket_lib.client import LocalClient
from util.json_util import CustomJsonEncoder
from util.log import error_trace

LOGGER = getLogger(__name__)
client = LocalClient(Config.FRONTEND_SERVER_PORT)


def func_with_retry(bind_func, max_retry=10, await_time=5):
    retry = 0

    while True:
        try:
            return bind_func()
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


def func_bool_if_except(bind_func):
    try:
        ret = bind_func()
        return (True, ret)
    except Exception as e:
        return (False, e)
