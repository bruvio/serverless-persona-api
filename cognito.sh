
aws cognito-idp admin-initiate-auth --cli-input-json file://auth.json

# aws cognito-idp admin-initiate-auth --user-pool-id us-east-1_1sUIpmKDD
# --client-id 550jdura2qfnhibnj67c2urqq0 --auth-flow ADMIN_NO_SRP_AUTH
# --auth-parameters USERNAME=bruno.viola@protonmail.com,PASSWORD=L1r1kp0p3n


aws cognito-idp admin-respond-to-auth-challenge --user-pool-id us-east-1_1sUIpmKDD --client-id 550jdura2qfnhibnj67c2urqq0 --challenge-name NEW_PASSWORD_REQUIRED --challenge-responses USERNAME=eeffe5b8-2e63-4285-ae3f-565700d66537,NEW_PASSWORD=L1r1kp0p3n --session AYABeO-Oye82kmLR9KFkQC0Ys3MAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHiAcAt7Ei832QLLvv5tnR-fAKEzaf-OMDg-j1aLh6qMVAG75Y4v-CIwQEJDJJbRkFkCAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMAFaEdp7QdXKqzsJ2AgEQgDs28JLNCNFPPn8N2JpkUGBrKT6fGrRRHfZZ2hIm1jCd74pl1Oeed2rrTy51eKvfFYeIfoIUKtHZZ8Lc4wIAAAAADAAAEAAAAAAAAAAAAAAAAAB6rJTGL_OCmSntygfhQSGt_____wAAAAEAAAAAAAAAAAAAAAEAAADVk0FXX54saBjch_djrMBzD0lzCVFYkAO2RTpJ0df9soSLqWUmiVhWApyvBNC6ki7vguneITwui-jumxHKFTiv4D-A_1hPqvHLLBqk1rcOq8PJyGd6JSpupwAYh5F9ywstsDefk4ge49fEVongooeGcA-js3qt_mFqxlNdDLOuR_asG0MgIxw3yYdIC11Fv8LpOr5SiQ7d5mV4z3iYyrQyRYOi-QAGeGp2cRUuL8Ct9c1d1xDT0fq6qzmbOwUDCOZ1V5-IddvuGPdsKlSKR4O2EwSITUqlEuKeNWyiL10iUyR-LKVVPw