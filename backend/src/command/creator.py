from importlib import import_module
from logging import getLogger

from command.commands import BaseCmd

LOGGER = getLogger(__name__)


class CommandCreator:
    @classmethod
    def create(cls, cmd_json) -> BaseCmd:
        LOGGER.debug(cmd_json)
        module = import_module("command.commands")
        cmd_class = getattr(module, cmd_json["_CommandName"])
        cmd = cmd_class(cmd_json)
        return cmd
