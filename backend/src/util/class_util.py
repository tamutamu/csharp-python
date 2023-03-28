class Singleton(object):
    @classmethod
    def I(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        else:
            pass
        return cls._instance
