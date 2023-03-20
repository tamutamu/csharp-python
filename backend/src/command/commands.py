import json
from logging import getLogger
from time import sleep

from command.base_command import BaseCmd
from db.manager import BackendResultManager
from model.models import StockPrice
from socket_lib.client import LocalClient
from util.jsonUtil import CustomJsonEncoder

LOGGER = getLogger(__name__)


class GetStockPriceCmd(BaseCmd):
    def main(self):
        brm = BackendResultManager()
        client = LocalClient()
        for i in range(10):
            stock_price = StockPrice()
            stock_price.open = i
            result = json.dumps(stock_price, cls=CustomJsonEncoder)
            brm.add(result)
            brm.commit()
            LOGGER.info(i)
            client.send(9999)
            sleep(8)

        return "ok end"
