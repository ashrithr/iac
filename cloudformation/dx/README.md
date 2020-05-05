
```
cd execute_sf
pip3 install --target . -r requirements.txt
cd ..

aws cloudformation package --template $PWD/template.yml \
--s3-bucket cw-us-east-1-167270772459-ashrith \
--s3-prefix functions \
--output-template-file template.pkg.yml

aws cloudformation deploy --stack-name dx-poc \
--template-file $PWD/template.pkg.yml \
--capabilities CAPABILITY_IAM \
--parameter-overrides (jq -r '.[] | [.ParameterKey, .ParameterValue] | join("=")' parameters.json)

aws cloudformation describe-stacks --stack-name dx-poc

aws cloudformation delete-stack --stack-name dx-poc
```