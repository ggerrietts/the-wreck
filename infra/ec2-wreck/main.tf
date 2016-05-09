
variable "node_name" {}
variable "db_ip_addr" {}

variable "dev_access_key" {}
variable "dev_secret_key" {}
variable "prd_access_key" {}
variable "prd_secret_key" {}

provider "aws" {
    alias       = "traceview-dev"
    region      = "us-east-1"
    access_key  = "${var.dev_access_key}"
    secret_key  = "${var.dev_secret_key}"
}

provider "aws" {
    alias       = "traceview-prod"
    region      = "us-east-1"
    access_key  = "${var.prd_access_key}"
    secret_key  = "${var.prd_secret_key}"
}

resource "aws_instance" "ec2_wreck" {
    provider                = "aws.traceview-dev"
    ami                     = "ami-9b49a8f6"
    instance_type           = "t2.medium"
    key_name                = "traceview-dev"
    vpc_security_group_ids  =  ["sg-1e827465"]
    tags {
        Name = "${var.node_name}.wreck"
    }
    connection {
      user = "ubuntu"
    }
    provisioner "remote-exec" {
      inline = ["rm -r /home/ubuntu/cookbooks", "mkdir /home/ubuntu/cookbooks"]
    }
    provisioner "file" {
      source = "../chef/vendor/"
      destination = "/home/ubuntu/cookbooks"
    }

    provisioner "file" {
      source = "provision-node.sh"
      destination = "/home/ubuntu/provision-node.sh"
    }

    provisioner "remote-exec" {
      inline = [
        "chmod +x /home/ubuntu/provision-node.sh",
        "provision-node.sh ${var.db_ip_addr} ${var.node_name}",

    }

    provisioner "remote-exec" {
      script = "do-chef-run.sh"
    }
}

resource "aws_route53_record" "cname" {
    provider        = "aws.traceview-prod"
    zone_id         = "Z2GWZH3I5TG4GH"
    name            = "${var.node_name}.wreck.tlys.us"
    type            = "CNAME"
    ttl             = "60"
    records         = ["${aws_instance.ec2_wreck.public_dns}"]
}


output "cname" { value = "${aws_route53_record.cname.fqdn}" }
output "ipaddr" { value = "${aws_instance.ec2_wreck.private_ip}" }

