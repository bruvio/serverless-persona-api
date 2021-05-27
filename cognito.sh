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
