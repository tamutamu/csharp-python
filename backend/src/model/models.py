from datetime import datetime

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
