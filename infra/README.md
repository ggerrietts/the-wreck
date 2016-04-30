
Building a new AMI with Packer required these steps:
1. Cd to `../chef`
2. Create `./vendor`
3. Execute `berks vendor vendor`
4. Execute `rm -r vendor/tw-*`
5. Cd to `../infra`
5. Run `packer build -var 'aws_access_key=XXX' -var 'aws_secret_key=XXX' the-wreck.packer.json`

My AMI gg-wreck-foundation has id 'ami-77cd2a1a'
