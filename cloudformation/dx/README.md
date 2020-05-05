
```
cd execute_sf
pip install --target . -r requirements.txt
cd ..

aws cloudformation package --template $PWD/template.yml \
--s3-bucket S3_BUCKET_NAME --output yaml > template.pkg.yml

aws cloudformation create-stack --stack-name dx-poc \
--template-body file://$PWD/template.pkg.yml \
--capabilities CAPABILITY_IAM \
--parameters file://$PWD/parameters.json

aws cloudformation describe-stacks --stack-name dx-poc

aws cloudformation delete-stack --stack-name dx-poc
```