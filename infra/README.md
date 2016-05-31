
Building a new AMI with Packer required these steps:
1. Cd to `../chef`
2. Create `./vendor`
3. Execute `berks vendor vendor`
4. Cd to `../infra`
5. Run `packer build -var-file=./.secret-vars.json the-wreck.packer.json`

My AMI gg-wreck-foundation has id 'ami-ced937a3' (but it's private, and you'll
want to build your own anyway)

Once you have a new AMI, you'll want to update ./ec2-wreck/main.tf with the new
AMI ID. You'll also need to adjust the DNS entries to something you control.
Then you should be able to terraform plan / terraform apply and spin up your own VMs.
