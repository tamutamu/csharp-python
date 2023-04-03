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


class SendResponse:
    def __init__(self, status: Const.Status, result: Const.Result, detail: str = ""):
        self.status = status
        self.result = result
        self.detail = detail


class SellRow:
    def __init__(self, product: AmazonProduct):
        self.asin = product.asin
        self.product = product

    action = ""
    status = ""
    sell_url = ""
    error_detail = ""


class SellDataByUser:
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
            create_key == SellDataByUser.__create_key
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

    def save(self, product: AmazonProduct):
        update_data = self.gen_serise_from_amazon_product(product)
        self.df.loc[product.asin] = update_data

    def save_row(self, sell_row: SellRow):
        update_data = self.gen_serise_from_amazon_product(sell_row.product)
        self.df.loc[sell_row.product.asin] = update_data
        self.df.to_csv(os.path.join(self.path, f"{self.user_id}.csv"), encoding="utf-8-sig", index=[0])

    def load(self, asin) -> SellRow:
        return SellRow()

    def get(self, asin) -> SellRow:
        row = self.df.loc[asin]

        for col in row.columns:
            print(col)

        return SellRow()

    def gen_serise_from_amazon_product(self, sell_row: SellRow):
        img_util = lambda i, n: i[n] if len(i) >= n + 1 else ""
        product = sell_row.product

        default_mapper = lambda index, row, field, model: model.setattr(field, row[index])

        dict_data = {
            "ASIN": {"field": "asin", "mapper": default_mapper},
            "ツールアクション": {"field": "ツールアクション", "mapper": default_mapper},
            "ステータス": {"status": default_mapper},
            "出品URL": {"sell_url": default_mapper},
            "エラー詳細": {"error_detail": default_mapper},
            "Amazon Title": {"title": default_mapper},
            "Amazon Description": {"desc": default_mapper},
            "Amazon Price": {"price": default_mapper},
            "Amazon Profit": {"profit_price": default_mapper},
            "Amazon Stock": {"stock": default_mapper},
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


class SendResponse:
    def __init__(self, status: Const.Status, result: Const.Result):
        self.status = status
        self.result = result
