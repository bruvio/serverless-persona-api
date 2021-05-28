# Serverless REST Persona API

The Persona API is a fake RESTful API that delivers made up data on a few endpoints. The data sits within a zip file and needs to be decompressed only on deployment.

## Deliverables

### Endpoints

You will need to deliver the following endpoints:

- GET /search/{username} Searches the data for the specific username
- GET /people Returns all people with pagination
- DELETE /people/{username} Delete a person

Produce a Swagger UI that will allow us to test the endpoints as a minimum.

### 1. Initial Setup

**Quick Setup** (prereq: `npm`)

```bash
npm install -g serverless
```

Detailed Setup Instructions [here](https://github.com/sejalv/serverless-workshop/blob/master/setup.md)

### 2. API

A CRUD application with a dockerized environment to test AWS services locally. Python for services and DynamoDB for database.

#### Project Structure:

Mono-repo style, i.e. service + IaaC

```
├──app/
    ├── __init__.py
    ├── handler.py
    ├── tests
    │   ├── __init__.py
    │   ├── conftest.py
    │   └── test_create.py
    │   └── test_delete.py
    │   └── test_get.py
    │   └── test_list.py
    └── utils
        ├── __init__.py
        ├── config.py
        └── helpers.py
        └── utility_dynamodb.py
├──.env
├──Dockerfile
├──docker-compose.yml
├──requirements.txt
├──serverless.yml
├──upload_data2S3.py
├──user_signup.py
├──pytest.ini
├──README.md


```

- `app/handler`: contains each CRUD function (create, retrieve/get, delete) that is executed by AWS Lambda, and associated with an API endpoint.
- `app/tests/`: Tests for Lambda handlers. Also includes `conftest.py` for `pytest` _fixtures_, that help in mocking or configuring your environment.
- `app/utils/`: Helpers functions
- `serverless.yml`: Serverless configuration for the service (or `app`). Includes IaaC to generate AWS components (`resources`), and attach `functions` for Lambda handlers, among other things.
- `docker-compose.yml`: includes
  - the default template from [LocalStack](https://github.com/localstack/localstack), an open-source framework that mimics AWS enviroment closely on your local setup
  - the build using [`lambci`](https://hub.docker.com/r/lambci/lambda/)'s Docker image to run and test the service locally.

### 4. Starting the Dev environment

`docker-compose build`

`docker-compose up`

NOTE: Build only if there's any change.

### 5. Tests

`docker-compose run app pytest tests/ -s -vv `

On the container for `app`, all the tests located within the `app/tests/` directory will run. This will also generate the AWS resources locally, via `app/tests/conftest.py` (eg. `ddb_tbl` fixture creates the DDB table `serverless-workshop-rest-ddb-test`).

`aws --endpoint-url=http://localhost:4566 ddb select serverless-workshop-rest-ddb-test`

Querying locally to check if the table is created. Also, creates an entry from the `test_create.py` test.

### 6. Deploy

**Optional Setup**:

`aws sso login --profile <profile-name>`

`yawsso`

In order to deploy the endpoint simply run

```bash
serverless deploy --stage <dev/stg>
```

This converts your `serverless.yml` config to a `CloudFormation` stack, and packages your service and dependencies
The expected result should be similar to:

```bash
Serverless: Packaging service…
Serverless: Uploading CloudFormation file to S3…
Serverless: Uploading service .zip file to S3…
Serverless: Updating Stack…
Serverless: Checking Stack update progress…
Serverless: Stack update finished…

Service Information
service: persona-api
stage: dev
region: us-east-1
stack: persona-api-dev
resources: 38
api keys:
  None
endpoints:
  GET - https://xxx.execute-api.us-east-1.amazonaws.com/dev/auth
  GET - https://xxx.execute-api.us-east-1.amazonaws.com/dev/people
  GET - https://xxx.execute-api.us-east-1.amazonaws.com/dev/username/{username}
  DELETE - https://xxx.execute-api.us-east-1.amazonaws.com/dev/delete/{username}
functions:
  test_auth: persona-api-dev-test_auth
  s3Event: persona-api-dev-s3Event
  list: persona-api-dev-list
  get: persona-api-dev-get
  delete: persona-api-dev-delete
layers:
  None

Stack Outputs
PersonaDynamoDbTableArn: persona-api-dev
DeleteLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:xxx:function:persona-api-dev-delete:38
AwsDocApiId: xxxx
GetLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:xxx:function:persona-api-dev-get:38
S3EventLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:xxx:function:persona-api-dev-s3Event:23
TestUnderscoreauthLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:xxx:function:persona-api-dev-test_auth:21
CognitoPoolClientId: xxxxxxxx
CognitoPoolId: us-east-xxx
ListLambdaFunctionQualifiedArn: arn:aws:lambda:us-east-1:xxx:function:persona-api-dev-list:23
ServiceEndpoint: https://xxx.execute-api.us-east-1.amazonaws.com/dev
DataIngestionS3Bucket: persona-api-data-dev
ServerlessDeploymentBucketName: bruvio-lambda-deployment-bucket
```

### 7. Usage (Post-Deployment)

You can create, retrieve, update, or delete todos with the following commands:

**via API Endpoints:**

### Get an Username

```bash
curl -X GET https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/get --data '{ "pathParameters": {"username":"kayleighlawrence"}}'
```

No output

### List all Usernames

```bash
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/people
```

### Get one Todo

```bash
# Replace the <username> part with a real username from your todos table
curl https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/username/<username>
```

### Delete a Todo

```bash
# Replace the <username> part with a real username from your todos table
curl -X DELETE https://XXXXXXX.execute-api.us-east-1.amazonaws.com/dev/delete/<username>
```

**via local CLI:**

`serverless invoke --function create --stage dev`

No output

### 8. Finally, destroy

Don't forget to remove the app from your AWS environment. Here's a clean way to do it with `serverless`

```bash
serverless remove --stage <dev/stg>
```

## Further Enhancements

### Scaling

#### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

#### DynamoDB

When you create a table, you specify how much provisioned throughput capacity you want to reserve for reads and writes. DynamoDB will reserve the necessary resources to meet your throughput needs while ensuring consistent, low-latency performance. You can change the provisioned throughput and increasing or decreasing capacity as needed.

This is can be done via settings in the `serverless.yml`. At the time of writing this README the write and read throughput capacities are set to 1

```yaml
ProvisionedThroughput:
  ReadCapacityUnits: 1
  WriteCapacityUnits: 1
```

In case you expect a lot of traffic fluctuation we recommend to checkout this guide on how to auto scale DynamoDB [https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/](https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/)

## References:

- https://www.serverless.com
- https://serverless-stack.com
- https://github.com/localstack/localstack
