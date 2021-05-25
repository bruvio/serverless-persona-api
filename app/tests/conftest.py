import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.dirname("__file__")))


@pytest.fixture(scope="session")
def event():
    event = {"pathParameters": {"username": "bruvio"}}
    return event


@pytest.fixture(scope="session")
def user():
    return "bruvio"
