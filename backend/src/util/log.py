import os
import sys
import traceback
from logging import getLogger


def error_trace(e: Exception):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname_line = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1] + f"({exc_tb.tb_lineno})"
    LOGGER = getLogger(fname_line)
    LOGGER.error(e)
    LOGGER.error(traceback.format_exc())
