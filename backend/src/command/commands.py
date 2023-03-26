import json
from logging import getLogger

from browser.driver.chrome import ChromeDriver
from command import CommandSessionManager
from command.base_command import BaseCmd
from config import Config
from db.manager import BackendResultManager
from model.models import StockPrice
from socket_lib.client import LocalClient
from util.jsonUtil import CustomJsonEncoder

LOGGER = getLogger(__name__)


class EventCmd(BaseCmd):
    def main(self):
        cmd = CommandSessionManager.I().get(self.cmd_json["process_id"])

        LOGGER.info("@@@@@@@@@@@")
        LOGGER.info(cmd)
        LOGGER.info(cmd.process_id)
        LOGGER.info(cmd.cmd_json)

        cmd.event.set()
        return Config.Const.OK


class PreLoginCmd(BaseCmd):
    """_summary_
    YahooとKeepaに事前ログインを行う
    """

    def main(self):
        brm = BackendResultManager(self.process_id)

        driver = ChromeDriver("test1", is_headless=False)
        driver.get("https://login.yahoo.co.jp/config/login")
        # self.event.clear()
        self.event.wait()

        client = LocalClient()
        client.send(Config.FRONTEND_SERVER_PORT, False)
        return "Login Success!!"


class GetStockPriceCmd(BaseCmd):
    def main(self):
        brm = BackendResultManager(self.process_id)
        client = LocalClient()
        for i in range(10):
            stock_price = StockPrice()
            stock_price.code = "test1"
            stock_price.open = i
            result = json.dumps(stock_price, cls=CustomJsonEncoder)
            brm.add(result)
            brm.commit()
            LOGGER.info(i)
            client.send(Config.FRONTEND_SERVER_PORT, False)

        return "ok end"
