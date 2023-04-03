from logging import getLogger
from time import sleep

from config import Config
from util.log_util import error_trace

LOGGER = getLogger(__name__)


def func_with_retry(func, max_retry=Config.MAX_RETRY, await_time=5, do_client_response=True):
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
                raise e


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
