from db.manager import get_session
from model.tables import BackendResult, SystemSetting
from util.log import error_trace


class BackendResultRepository:
    def __init__(self, process_id) -> None:
        self.id = process_id
        self.session = get_session()
        self.seq = 0

    def add(self, result):
        try:
            br = BackendResult()
            br.id = self.id
            br.seq = self.seq
            br.result = result
            self.session.add(br)
        except Exception as e:
            error_trace(e)
        finally:
            self.seq += 1

    def commit(self):
        self.session.commit()


class SystemSettingRepository:
    @classmethod
    def get(cls, name):
        return get_session().query(SystemSetting).get(name)

    @classmethod
    def list(cls):
        return get_session().query(SystemSetting).all()

    @classmethod
    def dict(cls):
        all = get_session().query(SystemSetting).all()
        return {e.name: e.value for e in all}

    @classmethod
    def add(cls, model):
        pass

    @classmethod
    def commit(self):
        self.session.commit()
