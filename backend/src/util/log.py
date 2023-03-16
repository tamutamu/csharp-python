import traceback
from logging import getLogger

LOGGER = getLogger()


def error_trace(e: Exception):
    LOGGER.error(e)
    LOGGER.error(traceback.format_exc())
