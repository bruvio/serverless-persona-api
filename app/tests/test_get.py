import pytest
import os
import sys
import logging

# from moto import mock_dynamodb2

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
import handler
from utils import config
from utils.helpers import get_ddb_resource

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# @mock_dynamodb2
@pytest.fixture(scope="function")
@pytest.mark.usefixtures("user")
def putUsername(user):
    context = None
    ddb_resource = get_ddb_resource(context)
    table = ddb_resource.Table(config.ddb_tbl_name)

    item = {"username": user}

    table.put_item(Item=item)
    logging.info("record created: " + str(item))


# @mock_dynamodb2
@pytest.mark.usefixtures("putUsername")
@pytest.mark.usefixtures("event")
def test_getUsername(event, context=None):
    logger.info("received this event \n {}".format(event))
    response = handler.get(event, context)
    # print(response)

    assert response["statusCode"] == 200
    # assert 200 == 200
    logger.info("get test success")
