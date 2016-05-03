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

module "db" {
  node_name = "db"
  source = "./ec2-wreck"
  dev_access_key  = "${var.dev_access_key}"
  dev_secret_key  = "${var.dev_secret_key}"
  prd_access_key  = "${var.prd_access_key}"
  prd_secret_key  = "${var.prd_secret_key}"
}

module "web" {
  node_name = "web"
  source = "./ec2-wreck"
  dev_access_key  = "${var.dev_access_key}"
  dev_secret_key  = "${var.dev_secret_key}"
  prd_access_key  = "${var.prd_access_key}"
  prd_secret_key  = "${var.prd_secret_key}"
}

module "traffic" {
  node_name = "traffic"
  source = "./ec2-wreck"
  dev_access_key  = "${var.dev_access_key}"
  dev_secret_key  = "${var.dev_secret_key}"
  prd_access_key  = "${var.prd_access_key}"
  prd_secret_key  = "${var.prd_secret_key}"
}

module "aux" {
  node_name = "aux"
  source = "./ec2-wreck"
  dev_access_key  = "${var.dev_access_key}"
  dev_secret_key  = "${var.dev_secret_key}"
  prd_access_key  = "${var.prd_access_key}"
  prd_secret_key  = "${var.prd_secret_key}"
}


