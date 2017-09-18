terraform {
  backend "s3" {
    region = "eu-west-2"
    bucket = "terraform-state-testy-test"
    key = "ec2-test.tfstate"
  }
}

provider "aws" {
  region = "eu-west-2"
}

variable public_key {}

resource "aws_key_pair" "test_key_pair" {
  key_name   = "key_pair"
  public_key = "${var.public_key}"
}

resource "aws_security_group" "test_security_group" {
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "test_ec2" {
  ami = "ami-e05a4d84"
  availability_zone = "eu-west-2a"
  instance_type = "t2.micro"
  key_name = "${aws_key_pair.test_key_pair.key_name}"
  vpc_security_group_ids = ["${aws_security_group.test_security_group.id}"]
  associate_public_ip_address = true

  tags {
    Name = "test-ec2"
  }
}

output "public_ip" {
  value = "${aws_instance.test_ec2.public_ip}"
}