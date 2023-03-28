import openpyxl

from db.repository import SystemSettingRepository


class Const:
    class Status:
        PENDING = "PENDING"
        RUNNING = "RUNNING"
        WAITING = "WAITING"
        EXIT = "EXIT"

    class Result:
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        SYSERR = "SYSERR"


class Config:
    DB_NAME = "main_db"
    PROFILE_NAME = "chrome"
    MAX_RETRY = 3
    BACKEND_SERVER_PORT = -1
    FRONTEND_SERVER_PORT = -1
    SETTING_FILE_PATH = None

    class Setting:
        AMAZON_USER_NAME = None
        AMAZON_USER_PASS = None


def load_setting():
    settings = SystemSettingRepository.dict()
    Config.SETTING_FILE_PATH = settings["SETTING_FILE_PATH"]

    wb = openpyxl.load_workbook(Config.SETTING_FILE_PATH)
    tool_setting = wb["ツール設定"]
    user_list = wb["ユーザ情報"]

    Config.Setting.AMAZON_USER_NAME = tool_setting["B4"].value
    Config.Setting.AMAZON_USER_PASS = tool_setting["B5"].value


# mypy: ignore-errors
# class _const:
#     class ConstError(TypeError):
#         pass

#     def __setattr__(self, name, value):
#         if name in self.__dict__:
#             raise self.ConstError("Can't rebind const (%s)" % name)
#         self.__dict__[name] = value


# import sys

# sys.modules["config"] = _const()
