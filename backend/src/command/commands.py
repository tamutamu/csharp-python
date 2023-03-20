import json
from logging import getLogger
from time import sleep

from command.base_command import BaseCmd
from db.manager import BackendResultManager
from model.modles import StockPrice
from util.jsonUtil import CustomJsonEncoder

LOGGER = getLogger(__name__)


class GetStockPriceCmd(BaseCmd):
    def main(self):
        brm = BackendResultManager()
        for i in range(10):
            stock_price = StockPrice()
            stock_price.open = i
            result = json.dumps(stock_price, cls=CustomJsonEncoder)
            brm.add(result)
            brm.commit()
            LOGGER.info(i)
            sleep(8)

        return "ok end"
