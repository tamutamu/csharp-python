import os
from datetime import datetime

import pandas as pd

from config import Const


class StockPrice:
    code = ""
    open = 0
    high = 0
    low = 0
    close = 0
    vol = 0
    date = datetime.now
    enable = True


class SendResponse:
    def __init__(self, status: Const.Status, result: Const.Result):
        self.status = status
        self.result = result


class SellManage:
    def __init__(self, path, user_id):
        self.df = pd.read_csv(
            os.path.join(path, f"{user_id}.csv"),
            index_col=[0],
            encoding="utf-8-sig",
        )
