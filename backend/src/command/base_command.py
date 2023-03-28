from abc import ABCMeta, abstractmethod
from logging import getLogger
from threading import Event, Thread
from time import sleep

from command.processor import CommandSessionManager
from config import Config
from util.log import error_trace

LOGGER = getLogger(__name__)


class CustomThread(Thread):
    # constructor
    def __init__(self, **kwargs):
        # execute the base constructor
        Thread.__init__(self, **kwargs)
        # set a default value
        self.value = None

    # function executed in a new thread
    def run(self):
        try:
            if self._target is not None:
                self.value = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


class BaseCmd(metaclass=ABCMeta):
    def __init__(self, cmd_json, process_id, is_async: bool = True) -> None:
        self.cmd_json = cmd_json
        self.is_async = is_async
        self.process_id = process_id
        self.event = Event()
        self.retry = 0

    def before(self):
        LOGGER.info(f"--- START[{self.cmd_json['_CommandName']}] ---")

    def __execute(self) -> None:
        self.before()
        ret = {}
        while Config.MAX_RETRY > self.retry:
            try:
                ret = self.main()
            except Exception as e:
                error_trace(e)
                self.retry += 1
                if Config.MAX_RETRY > self.retry:
                    LOGGER.error(f"再試行中... [{self.retry}回目]")
                    sleep(5)
                else:
                    LOGGER.error("処理失敗")
            finally:
                self.closing()
                
        self.after()
        return ret

    def execute(self) -> object:
        th = CustomThread(target=self.__execute, args=())
        th.daemon = True
        th.start()

        if self.is_async:
            return {"process_id": self.process_id}
        else:
            th.join()
            return th.value

    @abstractmethod
    def main(self) -> None:
        raise NotImplementedError()

    def closing(self) -> None:
        pass

    def after(self):
        CommandSessionManager.I().remove(self.process_id)
        LOGGER.info(f"--- END[{self.cmd_json['_CommandName']}] ---")
