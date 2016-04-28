provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "us-east-1"
}

resource "aws_instance" "example" {
    ami = "ami-b8b061d0"
    instance_type = "t1.micro"
}

resource "aws_eip" "ip" {
    instance = "${aws_instance.example.id}"
    depends_on = ["aws_instance.example"]
}

