import os
import boto3
import zipfile
import logging
import json
from botocore.exceptions import ClientError
import decimal
from utils import utility_dynamo
from utils import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3", use_ssl=False)

table_name = config.ddb_tbl_name
bucketname = config.ddb_bucket_name

dynamodbClient = boto3.client("dynamodb")
logger.debug("table is {}".format(table_name))
dynamodbResource = boto3.resource("dynamodb")
table = dynamodbResource.Table(table_name)


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
    response = {"statusCode": 500, "body": "An error occured while getting username."}
    data_id = event["pathParameters"]["username"]

    data_query = dynamodbClient.get_item(
        TableName=table_name, Key={"username": {"S": data_id}}
    )

    if "Item" in data_query:
        username = data_query["Item"]
        logger.info(f"username is: {username}")
        response = {
            "statusCode": 200,
            "body": json.dumps(utility_dynamo.to_dict(username)),
        }

    return response


def list(event, context):
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while getting all profiles.",
    }

    scan_result = dynamodbClient.scan(TableName=table_name)["Items"]

    users = []

    for user in scan_result:
        users.append(utility_dynamo.to_dict(user))

    response = {"statusCode": 200, "body": json.dumps(users)}

    return response


def delete(event, context):
    logger.info(f"Incoming request is: {event}")

    user_id = event["pathParameters"]["username"]
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": f"An error occured while deleting username {user_id}",
    }

    res = dynamodbClient.delete_item(
        TableName=table_name, Key={"username": {"S": user_id}}
    )

    # If deletion is successful for VIN
    if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
        response = {
            "statusCode": 204,
        }
    return response
