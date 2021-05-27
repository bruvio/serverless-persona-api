import os
import boto3
import zipfile
import logging
import json
import decimal
from botocore.exceptions import ClientError
import decimal
from app.utils import utility_dynamo
from app.utils import config, helpers

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3", use_ssl=False)

# table_name = config.ddb_tbl_name
# bucketname = config.ddb_bucket_name

# dynamodbClient = boto3.client("dynamodb")
# logger.debug("table is {}".format(table_name))
# dynamodbResource = boto3.resource("dynamodb")
# table = dynamodbResource.Table(table_name)


def s3Event(event, context):
    logger.debug(event)
    logger.debug(context)
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    # bucket='bruvio-persona-bucket'
    logger.info("unzipping data")

    err = unzip(bucket, key)
    if err == 0:
        logger.info("start to populate database")

        response, err = populate()

        logger.info("\n DONE")
        return response, err


def fill_table(table, table_data):
    """
    Fills an Amazon DynamoDB table with the specified data, using the Boto3
    Table.batch_writer() function to put the items in the table.
    Inside the context manager, Table.batch_writer builds a list of
    requests. On exiting the context manager, Table.batch_writer starts sending
    batches of write requests to Amazon DynamoDB and automatically
    handles chunking, buffering, and retrying.
    :param table: The table to fill.
    :param table_data: The data to put in the table. Each item must contain at least
                       the keys required by the schema that was specified when the
                       table was created.
    """
    try:
        with table.batch_writer() as writer:
            for item in table_data:
                writer.put_item(Item=item)
        logger.info("Loaded data into table %s.", table.name)
        return 0
    except ClientError:
        logger.exception("Couldn't load data into table %s.", table.name)
        return 1


def populate():

    table_name = config.ddb_tbl_name

    # dynamodbClient = boto3.client("dynamodb")
    logger.debug("table is {}".format(table_name))
    dynamodbResource = boto3.resource("dynamodb")
    table = dynamodbResource.Table(table_name)
    response = {"statusCode": 500, "body": "An error occured while populating table."}
    err = 1
    logger.info("\nreading data from s3")
    f = open("/tmp/fake_profiles.json")
    # Opening JSON file
    try:
        data = json.load(f, parse_float=decimal.Decimal)
        f.close()
    except JSONDecodeError:
        f.close()
        return response, err
    else:
        logger.info("\n populating table")
        err = fill_table(table, data)
        if err == 0:
            response = {
                "statusCode": 201,
            }
            err = 0
            return response, err
        return 1


def unzip(bucket, key):
    bucketname = config.ddb_bucket_name
    filename_json = "fake_profiles.json"  # replace with your object key
    try:
        s3.download_file(bucket, key, "/tmp/" + key)
    except:
        logger.error("failed to download file {}".format(key))
        return 1
    else:
        try:
            with zipfile.ZipFile("/tmp/" + key, "r") as zip_ref:
                zip_ref.extractall("/tmp/")
            logger.info("\nfile unzipped")
            os.chdir("/tmp/")
        except:
            logger.error("failed to unzip file {}".format(key))
            return 1
        else:
            try:
                s3.upload_file(filename_json, bucketname, filename_json)
                return 0
            except:
                logger.error("failed to upload file back to s3")
                return 1


def get(event, context):
    logger.info(f"Incoming request is: {event}")
    # Set the default error response
    ddb_resource = helpers.get_ddb_resource(context)
    table = ddb_resource.Table(config.ddb_tbl_name)
    data_id = event["pathParameters"]["username"]

    result = table.get_item(Key={"username": data_id})
    print(result)
    if "Item" in result:
        response = {
            "statusCode": 200,
            "body": json.dumps(result["Item"], cls=helpers.DecimalEncoder),
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(
                "{} not in database".format(data_id), cls=helpers.DecimalEncoder
            ),
        }

    return response


def list(event, context):
    # Set the default error response

    try:
        ddb_resource = helpers.get_ddb_resource(context)
        table = ddb_resource.Table(config.ddb_tbl_name)
        scan_result = table.scan()

        response = {
            "statusCode": 200,
            "body": json.dumps(scan_result["Items"], cls=helpers.DecimalEncoder),
        }
    except:
        response = {
            "statusCode": 500,
            "body": "An error occured while getting all profiles.",
        }

    return response


def delete(event, context):
    logger.info(f"Incoming request is: {event}")

    user_id = event["pathParameters"]["username"]
    # print(user_id)
    # Set the default error response
    response = generate_response(500, "An error occured while getting username.")
    ddb_resource = helpers.get_ddb_resource(context)
    table = ddb_resource.Table(config.ddb_tbl_name)
    res = table.delete_item(Key={"username": user_id})

    # If deletion is successful for username
    if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = {
            "statusCode": 204,
        }
        response = {
            "statusCode": 204,
            "body": json.dumps("True"),
        }
    return response


def generate_response(status, body, headers={}):
    return {
        "statusCode": status,
        "body": json.dumps(body, indent=4, cls=helpers.DecimalEncoder),
        "headers": headers,
    }


def endpoint_test_auth(event, context):
    return generate_response(200, {"bruvio": True})
