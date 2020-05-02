Package Lambda into zip file:

```
zip sample.zip index.py

aws s3 cp sample.zip s3://cw-us-east-1-167270772459-ashrith/functions/

aws cloudformation create-stack --stack-name deploy-lambda \
--template-body file://$PWD/template.yml \
--capabilities CAPABILITY_IAM \
--parameters ParameterKey=BucketName,ParameterValue=cw-us-east-1-167270772459-ashrith ParameterKey=S3Key,ParameterValue=functions/sample.zip

aws cloudformation describe-stacks --stack-name deploy-lambda

aws cloudformation delete-stack --stack-name deploy-lambda
```