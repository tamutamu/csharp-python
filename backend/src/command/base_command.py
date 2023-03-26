from abc import ABCMeta, abstractmethod
from logging import getLogger
from threading import Event, Thread

from command.processor import CommandSessionManager

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

    def before(self):
        LOGGER.info("--- START ---")

    def __execute(self) -> None:
        self.before()
        ret = self.main()
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

    def after(self):
        CommandSessionManager.I().remove(self.process_id)
        LOGGER.info("--- END ---")
