import pytest
import os
import sys
import json
import logging

sys.path.append(os.path.abspath(os.path.dirname("__file__")))

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_createTable(event, context, ddb_tbl):
    old_cnt = ddb_tbl.scan(Select="COUNT")["Count"]
    # create.handler(event, context)

    data = json.loads(event["pathParameters"])

    if "username" not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the user, username missing.")

    timestamp = str(datetime.utcnow())
    date = str(datetime.utcnow().date())
    ddb_resource = helpers.get_ddb_resource(context)
    table = ddb_resource.Table(config.ddb_tbl_name)

    item = {
        "username": data["username"],
        "createdAt": date,
        "updatedAt": timestamp,
    }

    table.put_item(Item=item)
    logging.info("record created: " + str(item))
    # create a response

    print(ddb_tbl.scan(Select="COUNT")["Count"])
    assert ddb_tbl.scan(Select="COUNT")["Count"] - old_cnt == 1
    logger.info("create test success")
