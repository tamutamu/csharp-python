import json
from logging import getLogger

from browser.amazon import Amazon
from browser.driver.chrome import ChromeDriver
from browser.yahoo import Yahoo
from command import CommandSessionManager
from command.base_command import BaseCmd
from config import Config, Const
from db.repository import BackendResultRepository
from model.models import SellManage, SendResponse, StockPrice
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

            for user_id, password, birth in Config.Setting.USER_LIST:
                self.sell_by_user(user_id, password, birth)

            response = SendResponse(Const.Status.WAITING, Const.Result.SUCCESS)
            self.client.send(response, False)
        except Exception as e:
            raise e
        finally:
            if self.amazon_driver is not None:
                self.amazon_driver.quit()
            if self.yahoo_driver is not None:
                self.yahoo_driver.quit()

    def sell_by_user(self, user_id, password, birth):
        sell_manage = SellManage("C:\\Users\\tamu0\\R\WORK\\csharp-python\\出品管理", user_id)
        for asin, item in sell_manage.df.iterrows():
            # Amazonデータ取得
            product = self.amazon_browser.get_product_data(asin)
            self.event.wait()

            # YahooAuction出品
            self.yahoo_browser.login(user_id, password)
            self.yahoo_browser.sell(product)


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
