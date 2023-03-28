import json
from datetime import date


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return {"_type": "date", "value": o.toordinal()}
        elif isinstance(o, object) and hasattr(o, "__dict__"):
            return o.__dict__
        else:
            return json.JSONEncoder.default(self, o)
