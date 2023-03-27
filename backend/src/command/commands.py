import json
from logging import getLogger

from selenium.webdriver.common.by import By

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
        cmd.event.set()
        return Config.Const.OK


class AmazonLoginCmd(BaseCmd):
    def main(self):
        brm = BackendResultManager(self.process_id)
        driver = ChromeDriver("test1", is_headless=False)
        driver.get(
            "https://www.amazon.co.jp/ap/signin?_encoding=UTF8&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"
        )

        driver.send_keys((By.ID, "ap_email"), self.cmd_json["amazon_user_name"])
        driver.click((By.ID, "continue"))

        driver.send_keys((By.ID, "ap_password"), self.cmd_json["amazon_user_pass"])
        driver.click((By.ID, "signInSubmit"))

        # self.event.clear()
        self.event.wait()
        # client = LocalClient()
        # client.send(Config.FRONTEND_SERVER_PORT, False)
        return Config.Const.OK


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
