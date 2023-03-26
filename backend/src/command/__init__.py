from logging import getLogger
from typing import Dict

from util.classUtil import Singleton

LOGGER = getLogger(__name__)


class CommandSessionManager(Singleton):
    def __init__(self):
        self.cmd_list: Dict[str, object] = dict()

    def add(self, id, cmd):
        self.cmd_list[id] = cmd

    def get(self, id):
        try:
            return self.cmd_list[id]
        except Exception as e:
            return None

    def remove(self, id):
        try:
            self.cmd_list.pop(id)
        except Exception as e:
            LOGGER.debug(e)
