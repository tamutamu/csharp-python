import json
from logging import getLogger

from command import CommandSessionManager
from command.creator import CommandCreator
from util.log_util import error_trace

LOGGER = getLogger(__name__)


class CommandProcessor:
    def process(self, req):
        try:
            LOGGER.debug(req)

            # コマンド生成、プロセスIDを生成・セット
            cmd = CommandCreator.create(json.loads(req))
            ret = cmd.execute()

            # waitをEventで解除する時など、どのコマンドセッションに実行するかをプロセスIDで管理
            CommandSessionManager.get_instance().add(cmd.process_id, cmd)

            return json.dumps(ret, ensure_ascii=False, indent=2)
        except Exception as e:
            error_trace(e)
