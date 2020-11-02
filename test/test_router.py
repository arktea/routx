import pytest

from routx import Router, Route


def homepage():
    return "Hello, world"


def users():
    return "All users"


def user(username):
    return f"User {username}"


def user_me():
    return "User fixed me"


def user_no_match():
    return "User fixed no match"


router = Router(
    [
        Route("/", endpoint=homepage, methods=["GET"]),
        Route("/users", endpoint=users),
        Route("/users/me", endpoint=user_me),
        Route("/users/{username}", endpoint=user),
        Route("/users/nomatch", endpoint=user_no_match)
    ]
)


def test_router():
    response = router.handle("/", "GET")
    assert response == "Hello, world"

    response = router.handle("/users", "GET")
    assert response == "All users"

    response = router.handle("/users/thibautfrain", "GET")
    assert response == "User thibautfrain"

    response = router.handle("/users/me", "GET")
    assert response == "User fixed me"

    # TODO : Manage redirects
    # response = router.handle("/users/thibautfrain/", "GET")
    # assert response == "User thibautfrain"

    response = router.handle("/users/nomatch", "GET")
    assert response == "User nomatch"
