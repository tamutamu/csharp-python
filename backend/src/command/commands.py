from abc import ABCMeta, abstractmethod
from logging import getLogger
from threading import Thread
from time import sleep

from db.manager import get_session
from model.modles import BackendResult

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
    def __init__(self, cmd_json, is_async: bool = True) -> None:
        self.cmd_json = cmd_json
        self.is_async = is_async

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
        self.thread_id = th.native_id

        if self.is_async:
            return {"thread_id": self.thread_id}
        else:
            th.join()
            return th.value

    @abstractmethod
    def main(self) -> None:
        raise NotImplementedError()

    def after(self):
        LOGGER.info("--- END ---")


class GetStockPriceCmd(BaseCmd):
    def main(self):
        LOGGER.info(self.__class__)
        sleep(6)

        br = BackendResult()
        br.thread_id = self.thread_id
        br.seq = 2
        br.result = "ok123"

        session = get_session()
        session.add(br)
        session.commit()

        return "ok123"
