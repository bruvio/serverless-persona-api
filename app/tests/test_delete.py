import pytest
import os
import sys
import logging

# from moto import mock_dynamodb2

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
import handler
from utils.helpers import get_ddb_resource
from utils import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# @mock_dynamodb2
@pytest.fixture(scope="function")
@pytest.mark.usefixtures("user")
def putUsername(user, context):
    ddb_resource = get_ddb_resource(context)
    table = ddb_resource.Table(config.ddb_tbl_name)

    item = {
        "username": user,
        # 'text': data['text'],
        # 'checked': False,
        # 'createdAt': date,
        # 'updatedAt': timestamp,
    }

    table.put_item(Item=item)
    logging.info("record created: " + str(item))
    # create a response


@pytest.mark.usefixtures("putUsername")
@pytest.mark.usefixtures("event")
def test_deleteUsername(event, context):
    logger.info("received this event \n {}".format(event))
    response = handler.delete(event, context)

    assert response["statusCode"] == 204
    logger.info("delete test success")
