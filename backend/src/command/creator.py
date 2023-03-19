import json
from logging import getLogger

from command.commands import BaseCmd, GetStockPriceCmd

LOGGER = getLogger(__name__)


class CommandCreator:
    @classmethod
    def create(cls, cmd_json) -> BaseCmd:
        LOGGER.debug(cmd_json)
        return GetStockPriceCmd(json.loads(cmd_json))
