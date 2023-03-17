import json
from logging import getLogger

from command.commands import BaseCmd
from util.log import error_trace

LOGGER = getLogger(__name__)


class CommandHandler:
    @classmethod
    def handle(cls, cmd: BaseCmd):
        try:
            ret = cmd.execute()
            return json.dumps(ret, ensure_ascii=False, indent=2)
        except Exception as e:
            error_trace(e)
