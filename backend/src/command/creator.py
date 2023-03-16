import json
from logging import getLogger

from command.commands import BaseCmd, GetStockPriceCmd

LOGGER = getLogger()


class CommandCreator:
    @classmethod
    def create(cls, cmd_json) -> BaseCmd:
        LOGGER.info(cmd_json)
        cmd_obj = json.loads(cmd_json)
        return GetStockPriceCmd(cmd_json)
