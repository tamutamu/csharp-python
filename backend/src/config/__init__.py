class Config:
    DB_NAME = "main_db"
    BACKEND_SERVER_PORT = -1
    FRONTEND_SERVER_PORT = -1

    class Const:
        OK = "OK"


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
