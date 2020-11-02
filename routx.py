import re
from urllib.parse import urlsplit


class Router:

    def __init__(self):
        self.routes = []

    def route(self, path, methods):

        def _route(f):
            path_regex, params = _path_regex(path)

            for method in methods:
                self.routes.append((path_regex, method, f, params))

        return _route

    def get(self, path):
        return self.route(path, methods=("GET",))

    def post(self, path):
        return self.route(path, methods=("POST",))

    def put(self, path):
        return self.route(path, methods=("PUT",))

    def delete(self, path):
        return self.route(path, methods=("DELETE",))

    def process(self, url, method):
        parts = urlsplit(url)

        for path_re, op, f, param_names in self.routes:
            if match := path_re.match(parts.path) \
                        and method.upper() == op.upper():

                params = {name: match.group(name) for name in param_names}

                return f(**params)

        raise Exception(f"No routes found for {method} {url}")


URL_REGEX = re.compile("{([^{}]*)?}")


def _path_regex(path):
    regex, idx = "", 0
    for match in URL_REGEX.finditer(path):
        regex += path[idx: match.start()]
        regex += f"(?P<{match.group(1)}>[^{{}}]*)"
        idx = match.end()
    regex += path[idx:-1]
    regex = re.compile(regex)
    return regex, list(regex.groupindex.keys())
