import os

ddb_tbl_name = os.environ.get("DYNAMODB_TABLE", "persona-api-dev")
ddb_bucket_name = os.environ.get("BUCKET", "persona-api-data-dev")
local_url = os.environ.get("LOCALSTACK_HOST", "http://localhost") + ":4566"
region_name = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
