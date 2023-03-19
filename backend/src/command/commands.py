from logging import getLogger

from command.base_command import BaseCmd
from db.manager import BackendResultManager

LOGGER = getLogger(__name__)


class GetStockPriceCmd(BaseCmd):
    def main(self):
        LOGGER.info(self.__class__)

        brm = BackendResultManager()
        result = "ok123"
        brm.add(result)
        brm.commit()

        return result
