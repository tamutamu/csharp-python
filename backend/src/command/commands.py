import json
from logging import getLogger

from selenium.webdriver.common.by import By

from browser.driver.chrome import ChromeDriver
from command import CommandSessionManager
from command.base_command import BaseCmd
from config import Config, Const
from db.repository import BackendResultRepository
from model.models import StockPrice
from socket_lib.client import LocalClient
from util.json_util import CustomJsonEncoder

LOGGER = getLogger(__name__)


class EventCmd(BaseCmd):
    def main(self):
        cmd = CommandSessionManager.I().get(self.cmd_json["process_id"])
        cmd.event.set()
        return Const.Result.SUCCESS


class AmazonLoginCmd(BaseCmd):
    def main(self):
        try:
            self.driver = ChromeDriver(Config.PROFILE_NAME, is_headless=False)

            self.driver.get(
                "https://www.amazon.co.jp/ap/signin?_encoding=UTF8&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"
            )

            self.driver.send_keys((By.ID, "ap_email"), Config.Setting.AMAZON_USER_NAME)
            self.driver.click((By.ID, "continue"))

            self.driver.send_keys((By.ID, "ap_password"), Config.Setting.AMAZON_USER_PASS)
            self.driver.click((By.ID, "signInSubmit"))
            # self.event.clear()

            # Waiting user action
            client = LocalClient()
            client.send({"status": Const.Status.WAITING}, Config.FRONTEND_SERVER_PORT, False)
            self.event.wait()
            return {"status": Const.Status.EXIT, "result": Const.Result.SUCCESS}

        except Exception as e:
            self.driver.quit()
            raise e


class GetStockPriceCmd(BaseCmd):
    def main(self):
        brm = BackendResultRepository(self.process_id)
        client = LocalClient()
        for i in range(10):
            stock_price = StockPrice()
            stock_price.code = "test1"
            stock_price.open = i
            result = json.dumps(stock_price, cls=CustomJsonEncoder)
            brm.add(result)
            brm.commit()
            LOGGER.info(i)
            client.send("", Config.FRONTEND_SERVER_PORT, False)

        return "ok end"
