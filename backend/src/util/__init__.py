import re


def normalize_money(price_text):
    if len(price_text) == 0:
        return 0
    else:
        return int(re.sub("[^0-9]", "", price_text))
