import boto3
import base64
import getpass
from botocore.exceptions import ClientError


def sign_up(app_client_id, username, password, cogPoolId):
    client = boto3.client("cognito-idp")

    try:
        sign_up_response = client.sign_up(
            ClientId=app_client_id, Username=username, Password=password
        )
        print(sign_up_response)

        confirm_sign_up_response = client.admin_confirm_sign_up(
            UserPoolId=cogPoolId, Username=username
        )
        print(confirm_sign_up_response)

    except ClientError as e:
        print(e)


def init_auth(app_client_id, username, password, cogPoolId):
    client = boto3.client("cognito-idp")

    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
        ClientId=app_client_id,
    )
    res = dict()
    res["AccessToken"] = response["AuthenticationResult"]["AccessToken"]
    res["IdToken"] = response["AuthenticationResult"]["IdToken"]
    res["RefreshToken"] = response["AuthenticationResult"]["RefreshToken"]
    print(response["AuthenticationResult"]["AccessToken"])
    print(response["AuthenticationResult"]["IdToken"])
    print(response["AuthenticationResult"]["RefreshToken"])
    return res


if __name__ == "__main__":
    cloudformation = boto3.resource("cloudformation")
    stackname = "persona-api-dev"

    cf_client = boto3.client("cloudformation")

    response = cf_client.describe_stacks(StackName=stackname)
    outputs = response["Stacks"][0]["Outputs"]
    for output in outputs:
        #
        keyName = output["OutputKey"]
        if keyName == "CognitoPoolId":
            cogPoolId = output["OutputValue"]
        if keyName == "CognitoPoolClientId":
            cogPoolClientId = output["OutputValue"]

    app_client_id = cogPoolClientId

    username = input("email address \n")
    pwd = base64.b64encode(getpass.getpass().encode("UTF-8")).decode("ascii")
    password = base64.b64decode(pwd.encode("ascii")).decode("UTF-8")
    sign_up(cogPoolClientId, username, password, cogPoolId)

    tokens = init_auth(app_client_id, username, password, cogPoolId)
