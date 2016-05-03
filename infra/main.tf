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

resource "aws_instance" "db_box" {
    provider                = "aws.traceview-dev"
    ami                     = "ami-40bb5a2d"
    instance_type           = "t2.medium"
    key_name                = "traceview-dev"
    vpc_security_group_ids  =  ["sg-aeb8a8ca", "sg-1a19dc7d"]
    tags {
        Name = "db.wreck"
    }
}

resource "aws_route53_record" "db_cname" {
    provider        = "aws.traceview-prod"
    zone_id         = "Z2GWZH3I5TG4GH"
    name            = "db.wreck.tlys.us"
    type            = "CNAME"
    ttl             = "60"
    records         = ["${aws_instance.db_box.public_dns}"]
}

resource "aws_instance" "traffic_box" {
    provider                = "aws.traceview-dev"
    ami                     = "ami-40bb5a2d"
    instance_type           = "t2.medium"
    key_name                = "traceview-dev"
    vpc_security_group_ids  =  ["sg-aeb8a8ca", "sg-1a19dc7d"]
    tags {
        Name = "traffic.wreck"
    }
}

resource "aws_route53_record" "traffic_cname" {
    provider        = "aws.traceview-prod"
    zone_id         = "Z2GWZH3I5TG4GH"
    name            = "traffic.wreck.tlys.us"
    type            = "CNAME"
    ttl             = "60"
    records         = ["${aws_instance.traffic_box.public_dns}"]
}

resource "aws_instance" "web_box" {
    provider                = "aws.traceview-dev"
    ami                     = "ami-40bb5a2d"
    instance_type           = "t2.medium"
    key_name                = "traceview-dev"
    vpc_security_group_ids  =  ["sg-aeb8a8ca", "sg-1a19dc7d"]
    tags {
        Name = "web.wreck"
    }
}

resource "aws_route53_record" "web_cname" {
    provider        = "aws.traceview-prod"
    zone_id         = "Z2GWZH3I5TG4GH"
    name            = "web.wreck.tlys.us"
    type            = "CNAME"
    ttl             = "60"
    records         = ["${aws_instance.web_box.public_dns}"]
}

resource "aws_instance" "aux_box" {
    provider                = "aws.traceview-dev"
    ami                     = "ami-40bb5a2d"
    instance_type           = "t2.medium"
    key_name                = "traceview-dev"
    vpc_security_group_ids  =  ["sg-aeb8a8ca", "sg-1a19dc7d"]
    tags {
        Name = "aux.wreck"
    }
}

resource "aws_route53_record" "aux_cname" {
    provider        = "aws.traceview-prod"
    zone_id         = "Z2GWZH3I5TG4GH"
    name            = "aux.wreck.tlys.us"
    type            = "CNAME"
    ttl             = "60"
    records         = ["${aws_instance.aux_box.public_dns}"]
}

