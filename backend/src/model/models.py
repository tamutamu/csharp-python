import os
from datetime import datetime

import pandas as pd

from config import Config, Const


class StockPrice:
    code = ""
    open = 0
    high = 0
    low = 0
    close = 0
    vol = 0
    date = datetime.now
    enable = True


class AmazonProduct:
    def __init__(self, asin):
        self.asin = asin

    title = ""
    price = 0
    img_list = []
    desc = ""
    stock = ""

    @property
    def profit_price(self):
        # (価格 + 固定費) × 利益率
        return int((self.price + Config.Setting.FIXED_COST) * ((Config.Setting.PROFIT_RATE + 100) / 100))


class SellRow:
    def __init__(self, asin, amazon_product: AmazonProduct):
        self.asin = asin
        self.amazon_product = amazon_product

    action = ""
    status = 0
    sell_url = ""
    error_detail = ""


class SendResponse:
    def __init__(self, status: Const.Status, result: Const.Result, detail: str = ""):
        self.status = status
        self.result = result
        self.detail = detail


class SellManageByUser:
    __create_key = object()
    _instance_map = dict()

    @classmethod
    def I(cls, path, user_id):
        key = f"{path}-{user_id}"

        if key not in cls._instance_map:
            cls._instance_map[key] = cls(cls.__create_key, path, user_id)

        return cls._instance_map[key]

    def __init__(self, create_key, path, user_id):
        assert (
            create_key == SellManageByUser.__create_key
        ), "OnlyCreatable objects must be created using OnlyCreatable.create"

        self.path = path
        self.user_id = user_id

        df = pd.read_csv(
            os.path.join(path, f"{user_id}.csv"),
            index_col=[0],
            encoding="utf-8-sig",
        )

        dup_df = df[df.index.duplicated()]
        if len(dup_df) > 0:
            raise Exception("Asinが重複しています")

        self.df = df

    def save(self, sell_row: SellRow):
        update_data = self.gen_serise_from_amazon_product(product)
        self.df.loc[product.asin] = update_data
        self.df.to_csv(os.path.join(self.path, f"{self.user_id}.csv"), encoding="utf-8-sig", index=[0])

    def load(self, asin) -> SellRow:
        return SellRow()

    def gen_serise_from_amazon_product(self, product: AmazonProduct, sell_result):
        img_util = lambda i, n: i[n] if len(i) >= n + 1 else ""

        dict_data = {
            "ASIN": product.asin,
            "ツールアクション": "",
            "ステータス": "",
            "出品URL": "",
            "エラー詳細": "",
            "Amazon Title": product.title,
            "Amazon Description": product.desc,
            "Amazon Price": product.price,
            "Amazon Profit": product.profit_price,
            "Amazon Stock": product.stock,
            "Amazon Image0": img_util(product.img_list, 0),
            "Amazon Image1": img_util(product.img_list, 1),
            "Amazon Image2": img_util(product.img_list, 2),
            "Amazon Image3": img_util(product.img_list, 3),
            "Amazon Image4": img_util(product.img_list, 4),
            "Amazon Image5": img_util(product.img_list, 5),
            "Amazon Image6": img_util(product.img_list, 6),
            "Amazon Image7": img_util(product.img_list, 7),
            "Amazon Image8": img_util(product.img_list, 8),
            "Amazon Image9": img_util(product.img_list, 9),
        }

        return pd.Series(dict_data)
