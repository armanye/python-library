import json


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder.

    json.dumps(some_class) doesnt work beause some objects arent
    serializable so this basically ignores them.
    """

    def default(self, o):
        data = {}
        for k, v in o.__dict__.items():
            if (
                isinstance(v, int)
                or isinstance(v, float)
                or isinstance(v, str)
                or isinstance(v, bool)
                or isinstance(v, dict)
                or isinstance(v, list)
            ):
                data[k] = v
        return data
