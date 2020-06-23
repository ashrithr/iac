# s3-kms

```
aws cloudformation deploy --stack-name s3-kms-iam \
  --template-file $PWD/template.yml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides AdminRoleId=(aws iam get-role --role-name GSuiteAdministrators --query "Role.RoleId")
```