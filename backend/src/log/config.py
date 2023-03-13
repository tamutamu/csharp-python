from logging import getLogger
from logging.config import dictConfig
from ruamel.yaml import YAML
from pathlib import Path
from time import sleep

def init_logging():
    """ ログのローテーション設定 """
    config_path = Path('./logging.yml')
    config_value = YAML().load(config_path)
    dictConfig(config_value)