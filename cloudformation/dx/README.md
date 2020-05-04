
```
zip export_dataset.zip export_dataset.py
zip monitor_export.zip monitor_export.py

aws s3 cp export_dataset.zip s3://S3_BUCKET_NAME/functions/
aws s3 cp monitor_export.zip s3://S3_BUCKET_NAME/functions/

aws cloudformation create-stack --stack-name dx-poc \
--template-body file://$PWD/template.yml \
--capabilities CAPABILITY_IAM \
--parameters file://$PWD/parameters.json

aws cloudformation describe-stacks --stack-name dx-poc

aws cloudformation delete-stack --stack-name dx-poc
```