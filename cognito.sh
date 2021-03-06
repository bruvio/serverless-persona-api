#!/usr/bin/env bash

export REGION="us-east-1"
export stackName="persona-api-dev"
export CognitoUserPoolId=$(aws cloudformation describe-stacks --stack-name $stackName --query 'Stacks[0].Outputs[?OutputKey==`CognitoPoolId`].OutputValue' --output text)
export CognitoPoolClientId=$(aws cloudformation describe-stacks --stack-name $stackName --query 'Stacks[0].Outputs[?OutputKey==`CognitoPoolClientId`].OutputValue' --output text)


echo region is $REGION
echo stackName is $stackName
echo CognitoUserPoolId is $CognitoUserPoolId
echo CognitoPoolClientId is $CognitoPoolClientId


aws cognito-idp sign-up \
  --region $REGION \
  --client-id $CognitoPoolClientId \
  --username bruno.viola@protonmail.com \
  --password Passw0rd!

aws cognito-idp admin-confirm-sign-up \
  --region $REGION \
  --user-pool-id $CognitoUserPoolId \
  --username bruno.viola@protonmail.com



sed -e "s|\${CognitoUserPoolId}|$CognitoUserPoolId|" -e "s|\${CognitoPoolClientId}|$CognitoPoolClientId|" auth_template.json > auth.json

aws cognito-idp admin-initiate-auth --cli-input-json file://auth.json


# aws cognito-idp admin-initiate-auth --cli-input-json file://auth_new.json

# aws cognito-idp admin-initiate-auth --user-pool-id us-east-1_1sUIpmKDD
# --client-id 550jdura2qfnhibnj67c2urqq0 --auth-flow ADMIN_NO_SRP_AUTH
# --auth-parameters USERNAME=xxxx,PASSWORD=xxxxx

# 12a980ca-b5d8-4e9e-86d0-d5b3bb2517a3

# aws cognito-idp admin-respond-to-auth-challenge --user-pool-id us-east-1_Bi8OH7iCT --client-id 4bld268vfouhqfn2ljo2h0tup2 --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses USERNAME=1436190c-5ac6-4633-8052-875c60f1066a,NEW_PASSWORD=xxxx --session AYABeMKFl2saVDEBV-fiCo8-jlkAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHiAcAt7Ei832QLLvv5tnR-fAKEzaf-OMDg-j1aLh6qMVAFea6AwC9dLzzvK_ZHcMjUtAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMvhlbwtdq1XbtaDemAgEQgDvHo772-pfjjzzwv10TVY5XT_9SZbN4grgqofx61Lk9qpyOqCOdFeNPwzAxWGNaDqgvg7IA9AwCS7IZAQIAAAAADAAAEAAAAAAAAAAAAAAAAACY9swLvpf_d4YKarA6xMKR_____wAAAAEAAAAAAAAAAAAAAAEAAADVEaYJ3egoMbAM7FonC8J8dNQK1TpfwkfRoIhxMrYAg1etEqhxz-Vah3STPKoGJf7dO6ZQLaUV28rmBteWSlfB5L-JuDg5AaQpJK1UAkWfZOZvcGvNvJabQCNsx1HhJzsCjT5_JWDFSrPRYxerfS4E5US_D6yoDaZ-thwxbwL9PxJzOIlOTxDoW4yH_aeWl7COWppo7UPe5UFOclbYtRLaSfpBOps06zSdzliplqx4uXWH2T9UTsql__yX2e-CHsW7hLTBoxxenT4prVL8HH4Jh_GEeHjJHCz-fA9zI72CHRVSGSu79g



# aws cognito-idp admin-create-user \
#     --user-pool-id us-east-1_1sUIpmKDD \
#     --username brn.viola@gmail.com \
#     --user-attributes Name=email,Value=brn.viola@gmail.com \
#     --message-action SUPPRESS

# aws cognito-idp admin-set-user-password \
#   --user-pool-id us-east-1_1sUIpmKDD \
#   --username xxxxx \
#   --password xxx \
#   --permanent

# aws cognito-idp admin-confirm-sign-up --user-pool-id us-east-1_1sUIpmKDD --username xxx
