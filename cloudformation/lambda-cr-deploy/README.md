Example Lambda based CFT Custom Resource:

```
pip install --target ./package -r requirements.txt
cd package
zip -r9 ../cr.zip .
cd ..
zip -g cr.zip cr.py

aws s3 cp cr.zip s3://S3_BUCKET_NAME/functions/

aws cloudformation create-stack --stack-name deploy-lambda-cr \
--template-body file://$PWD/template.yml \
--capabilities CAPABILITY_IAM \
--parameters ParameterKey=BucketName,ParameterValue=S3_BUCKET_NAME ParameterKey=S3Key,ParameterValue=functions/cr.zip

aws cloudformation describe-stacks --stack-name deploy-lambda-cr

aws cloudformation delete-stack --stack-name deploy-lambda-cr
```