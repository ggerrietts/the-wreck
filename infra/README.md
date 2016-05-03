
Building a new AMI with Packer required these steps:
1. Cd to `../chef`
2. Create `./vendor`
3. Execute `berks vendor vendor`
4. Execute `rm -r vendor/tw-*`
5. Cd to `../infra`
5. Run `packer build -var-file=./.secret-vars the-wreck.packer.json`

My AMI gg-wreck-foundation has id 'ami-a858bec5'
