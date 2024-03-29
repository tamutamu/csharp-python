import functools
import json
from logging import getLogger

from browser.amazon import Amazon
from browser.driver.chrome import ChromeDriver
from browser.yahoo import YahooAuction
from command import CommandSessionManager
from command.base_command import BaseCmd
from config import Config, Const
from db.repository import BackendResultRepository
from model.models import SellOfUser, SendResponse, StockPrice
from util.func_util import func_with_retry
from util.json_util import CustomJsonEncoder

LOGGER = getLogger(__name__)


class EventCmd(BaseCmd):
    def main(self):
        cmd = CommandSessionManager.get_instance().get(self.cmd_json["process_id"])
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

            self.yahoo_driver = ChromeDriver(is_headless=False, incognito=True)
            self.ya_browser = YahooAuction(self.yahoo_driver)

            for user_id, password, birth in Config.Setting.USER_LIST:
                self.sell(user_id, password, birth)
                response = SendResponse(Const.Status.WAITING, Const.Result.SUCCESS)
                self.client.send(response, False)

        except Exception as e:
            raise e
        finally:
            if self.amazon_driver is not None:
                self.amazon_driver.quit()
            if self.yahoo_driver is not None:
                self.yahoo_driver.quit()

    def sell(self, user_id, password, birth):
        sell_of_user = SellOfUser.get_instance("..\\出品管理", user_id)
        self.ya_browser.login(user_id, password)

        for asin, item in sell_of_user.df.iterrows():
            sell_row = self.sell_by_user(asin, sell_of_user)
            sell_of_user.update_row(sell_row)

    def sell_by_user(self, asin, sell_manage_by_user: SellOfUser):
        # Amazonデータ取得
        bind_func = functools.partial(self.amazon_browser.get_product_data, asin)
        product = func_with_retry(bind_func)

        # YahooAuction出品
        bind_func = functools.partial(self.ya_browser.new_sell, product)
        sell_row = func_with_retry(bind_func)

        return sell_row

    def update_sell_by_user(self, asin, sell_manage_by_user: SellOfUser):
        pass

    def delete_sell_by_user(self, asin, sell_manage_by_user: SellOfUser):
        pass


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
