import re
from typing import List, Tuple, Dict, Any, Callable, Pattern

from routx.convertor import CONVERTOR_TYPES, Convertor


class Route:

    def __init__(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str] = None
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.methods = ["GET"] if methods is None else list(methods)
        self.path_regex, self.params = compile_path(path)


class Router:

    def __init__(
        self,
        routes: List[Route] = None
    ) -> None:
        self.routes = [] if routes is None else routes

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str] = None
    ) -> None:
        self.routes.append(
            Route(
                path,
                endpoint,
                methods=methods
            )
        )

    def route(
        self,
        path: str,
        methods: List[str] = None
    ) -> Callable:

        def decorator(func: Callable):
            self.add_route(
                path,
                func,
                methods=methods
            )

        return decorator

    def get(
        self,
        path: str
    ) -> Callable:
        return self.route(path, methods=["GET"])

    def post(
        self,
        path: str
    ) -> Callable:
        return self.route(path, methods=["POST"])

    def put(
        self,
        path: str
    ) -> Callable:
        return self.route(path, methods=["PUT"])

    def delete(
        self,
        path: str
    ) -> Callable:
        return self.route(path, methods=["DELETE"])

    def handle(
        self,
        path: str,
        method: str
    ) -> Any:
        for route in self.routes:
            match = route.path_regex.match(path)
            if match and method in route.methods:
                params = {name: match.group(name) for name in route.params}
                return route.endpoint(**params)

        raise Exception(f"No routes found for {method} {path}")


PARAM_RE = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}")


def compile_path(
    path: str
) -> Tuple[Pattern, Dict[str, Convertor]]:

    path_regex = "^"
    idx = 0
    param_convertors = {}

    for match in PARAM_RE.finditer(path):
        param_name, convertor_type = match.groups("str")
        convertor = CONVERTOR_TYPES[convertor_type]

        path_regex += re.escape(path[idx:match.start()])
        path_regex += f"(?P<{param_name}>{convertor.regex})"

        param_convertors[param_name] = convertor
        idx = match.end()

    path_regex += re.escape(path[idx:]) + "$"

    return re.compile(path_regex), param_convertors
