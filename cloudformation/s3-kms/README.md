# s3-kms

```
aws cloudformation deploy --stack-name s3-kms \
--template-file $PWD/template.yml \
--capabilities CAPABILITY_IAM \
--parameters ParameterKey=AdminRoleId,ParameterValue=(aws iam get-role --role-name GSuiteAdministrators --query "Role.RoleId")
```