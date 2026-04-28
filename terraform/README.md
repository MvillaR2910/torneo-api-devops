# Terraform Deployment Guide

This folder contains the AWS infrastructure definition for the `torneo-api` project.

## Resources Created

- 1 VPC
- 2 public subnets
- 1 internet gateway
- 1 public route table
- 1 EC2 instance for the FastAPI app
- 1 PostgreSQL RDS instance
- 2 security groups
- 1 DB subnet group

## Files

- `provider.tf`: AWS provider and Terraform version.
- `variables.tf`: Input variables for the deployment.
- `vpc.tf`: Main VPC resource.
- `network.tf`: Subnets, internet gateway and route table.
- `security_groups.tf`: Firewall rules for EC2 and RDS.
- `ec2.tf`: EC2 instance used to host the API.
- `rds.tf`: PostgreSQL database on RDS.
- `outputs.tf`: Useful outputs after apply.
- `terraform.tfvars.example`: Example variable values.

## Before Running Terraform

1. Install Terraform on your machine.
2. Install and configure the AWS CLI.
3. Create an EC2 key pair in AWS and save the `.pem` file locally.
4. Copy `terraform.tfvars.example` to `terraform.tfvars`.
5. Replace the example values with your real AWS and database settings.

## Commands

```bash
terraform init
terraform plan
terraform apply
```

To destroy everything when you finish:

```bash
terraform destroy
```

## Notes

- The EC2 instance opens port `8000` for the FastAPI app.
- The RDS instance is not public; only the EC2 instance can reach it.
- You should connect to EC2 over SSH and from there test the database connection with `psql`.
