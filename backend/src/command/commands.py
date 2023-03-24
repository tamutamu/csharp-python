import json
from logging import getLogger
from time import sleep

from browser.driver.chrome import ChromeDriver
from command.base_command import BaseCmd
from config import Config
from db.manager import BackendResultManager
from model.models import StockPrice
from socket_lib.client import LocalClient
from util.jsonUtil import CustomJsonEncoder

LOGGER = getLogger(__name__)


class PreLoginCmd(BaseCmd):
    """_summary_
    YahooとKeepaに事前ログインを行う
    """

    def main(self):
        brm = BackendResultManager(self.process_id)

        driver = ChromeDriver("test1", is_headless=False)
        driver.get("https://login.yahoo.co.jp/config/login")
        input("Login OK?")

        client = LocalClient()
        client.send(Config.FRONTEND_SERVER_PORT, False)
        return "Login Success!!"


class GetStockPriceCmd(BaseCmd):
    def main(self):
        brm = BackendResultManager(self.process_id)
        client = LocalClient()
        for i in range(10):
            stock_price = StockPrice()
            stock_price.open = i
            result = json.dumps(stock_price, cls=CustomJsonEncoder)
            brm.add(result)
            brm.commit()
            LOGGER.info(i)
            client.send(Config.FRONTEND_SERVER_PORT, False)
            sleep(8)

        return "ok end"
