import pytest
import os
import sys

# from moto import mock_dynamodb2
import logging

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
print(os.path.abspath(os.path.dirname("__file__")))
import handler


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@pytest.fixture(scope="function")
def event():
    event = {}
    return event


# @mock_dynamodb2
@pytest.mark.usefixtures("event")
def test_List(event, context=None):
    logger.info("received this event \n {}".format(event))
    response = handler.list(event, context)

    assert response["statusCode"] == 200
    logger.info("list test success")
