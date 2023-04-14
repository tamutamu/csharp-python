import functools
import os
from datetime import datetime
import re

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

        self.action = ""
        self.status = ""
        self.sell_url = ""
        self.error_detail = ""

        # Amazonデータ
        self.product = product


class SellOfUser:
    __create_key = object()
    _instance_map = dict()

    @classmethod
    def get_instance(cls, path, user_id):
        key = f"{path}-{user_id}"

        if key not in cls._instance_map:
            cls._instance_map[key] = cls(cls.__create_key, path, user_id)

        return cls._instance_map[key]

    def __init__(self, create_key, path, user_id):
        assert create_key == SellOfUser.__create_key, "OnlyCreatable objects must be created using OnlyCreatable.create"

        self.path = path
        self.user_id = user_id

        df = pd.read_csv(
            os.path.join(path, f"{user_id}.csv"),
            index_col=[0],
            encoding="utf-8-sig",
        ).fillna("")

        dup_df = df[df.index.duplicated()]
        if len(dup_df) > 0:
            raise Exception("Asinが重複しています")

        self.df = df

    def update_row(self, sell_row: SellRow):
        update_data = self.gen_sell_row_serise(sell_row)
        self.df.loc[sell_row.product.asin] = update_data
        self.df.to_csv(os.path.join(self.path, f"{self.user_id}.csv"), encoding="utf-8-sig", index=[0])

    def get_sell_row(self, asin) -> SellRow:
        row = self.df.loc[asin]

        for col in row.columns:
            print(col)

        return SellRow()

    def rgetattr(self, obj, attr, *args):
        def _getattr(obj, attr):
            array_result = re.match(r"(.*)\[(\d+)\]", attr)
            if array_result:
                _attr = array_result.groups()[0]
                _index = int(array_result.groups()[1])
                _img_list = getattr(obj, _attr, *args)
                if len(_img_list) > _index + 1:
                    return getattr(obj, _attr, *args)[_index]
                else:
                    return ""
            else:
                return getattr(obj, attr, *args)

        return functools.reduce(_getattr, [obj] + attr.split("."))

    def sell_row_to_dict(self, sell_row):
        mapping = {
            "ASIN": "asin",
            "ツールアクション": "action",
            "ステータス": "status",
            "出品URL": "sell_url",
            "エラー詳細": "error_detail",
            "Amazon Title": "product.title",
            "Amazon Description": "product.desc",
            "Amazon Price": "product.price",
            "Amazon Profit": "product.profit_price",
            "Amazon Stock": "product.stock",
            "Amazon Image0": "product.img_list[0]",
            "Amazon Image1": "product.img_list[1]",
            "Amazon Image2": "product.img_list[2]",
            "Amazon Image3": "product.img_list[3]",
            "Amazon Image4": "product.img_list[4]",
            "Amazon Image5": "product.img_list[5]",
            "Amazon Image6": "product.img_list[6]",
            "Amazon Image7": "product.img_list[7]",
            "Amazon Image8": "product.img_list[8]",
            "Amazon Image9": "product.img_list[9]",
        }

        sell_row_dict = dict()
        for key, prop_name in mapping.items():
            sell_row_dict[key] = self.rgetattr(sell_row, prop_name)

        return sell_row_dict

    def gen_sell_row_serise(self, sell_row: SellRow):
        import ipdb

        ipdb.set_trace()
        dict_data = self.sell_row_to_dict(sell_row)
        return pd.Series(dict_data)
