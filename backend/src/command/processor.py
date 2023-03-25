import json
from logging import getLogger

from command.creator import CommandCreator
from util.log import error_trace

LOGGER = getLogger(__name__)


class CommandProcessor:
    def process(self, req):
        try:
            LOGGER.info(req)
            cmd = CommandCreator.create(json.loads(req))
            ret = cmd.execute()
            LOGGER.info("execte end..1")
            LOGGER.info(ret)
            LOGGER.info("execte end..2")
            return json.dumps(ret, ensure_ascii=False, indent=2)
        except Exception as e:
            error_trace(e)
