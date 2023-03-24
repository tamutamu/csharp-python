import json
from logging import getLogger

from command.creator import CommandCreator
from util.log import error_trace

LOGGER = getLogger(__name__)


class CommandProcessor:
    def process(self, req):
        try:
            cmd = CommandCreator.create(json.loads(req))
            ret = cmd.execute()
            return json.dumps(ret, ensure_ascii=False, indent=2)
        except Exception as e:
            error_trace(e)
