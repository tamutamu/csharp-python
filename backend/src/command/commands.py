import json
from logging import getLogger
import pandas as pd
import os

from browser.driver.chrome import ChromeDriver
from command import CommandSessionManager
from browser.amazon import Amazon
from command.base_command import BaseCmd
from browser.yahoo import Yahoo
from config import Config, Const
from db.repository import BackendResultRepository
from model.models import SendResponse, StockPrice
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
            self.amazon_driver = ChromeDriver(Config.AMAZON_PROFILE_NAME, is_headless=False)

            amazon = Amazon(self.amazon_driver)
            amazon.login(Config.Setting.AMAZON_USER_NAME, Config.Setting.AMAZON_USER_PASS)

            # Waiting user action
            response = SendResponse(Const.Status.WAITING, Const.Result.SUCCESS)
            response.process_id = self.process_id
            self.client.send(response, False)

            self.event.wait()
        except Exception as e:
            raise e
        finally:
            if self.amazon_driver is not None:
                self.amazon_driver.quit()


class YahooAuctionSellCmd(BaseCmd):
    def main(self):
        try:
            self.amazon_driver = ChromeDriver(Config.AMAZON_PROFILE_NAME, is_headless=False)
            self.amazon_browser = Amazon(self.amazon_driver)

            self.yahoo_driver = ChromeDriver(is_headless=False)
            self.yahoo_browser = Yahoo(self.yahoo_driver)

            for username, password, birth in Config.Setting.USER_LIST:
                self.sell_by_user(username, password, birth)

            response = SendResponse(Const.Status.WAITING, Const.Result.SUCCESS)
            self.client.send(response, False)
        except Exception as e:
            raise e
        finally:
            if self.amazon_driver is not None:
                self.amazon_driver.quit()
            if self.yahoo_driver is not None:
                self.yahoo_driver.quit()

    def sell_by_user(self, username, password, birth):
        df_sell = pd.read_csv(
            os.path.join("C:/Users/naoki/R/WORK/csharp-python/出品管理", f"{username}.csv"),
            index_col=[0],
            encoding="utf-8-sig",
        )

        for asin, item in df_sell.iterrows():
            # Amazonデータ取得
            product = self.amazon_browser.get_product_data(asin)

            # YahooAuction出品
            self.yahoo_browser.login(username, password)
            self.yahoo_browser.sell(product)

            self.event.wait()


class GetStockPriceCmd(BaseCmd):
    def main(self):
        brm = BackendResultRepository(self.process_id)
        for i in range(10):
            stock_price = StockPrice()
            stock_price.code = "test1"
            stock_price.open = i
            result = json.dumps(stock_price, cls=CustomJsonEncoder)
            brm.add(result)
            brm.commit()
            LOGGER.info(i)

        return "ok end"
