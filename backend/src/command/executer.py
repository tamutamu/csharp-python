from logging import getLogger

from command.commands import BaseCmd
from util.log import error_trace

LOGGER = getLogger()


class CommandHandler:
    @classmethod
    def handle(cls, cmd: BaseCmd):
        try:
            return cmd.execute()
        except Exception as e:
            error_trace(e)
