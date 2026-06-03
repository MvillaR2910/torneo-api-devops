variable "project_name" {
  description = "Base name for all AWS resources."
  type        = string
  default     = "torneo-api"
}

variable "aws_region" {
  description = "AWS region for the deployment."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_1_cidr" {
  description = "CIDR block for the first public subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_2_cidr" {
  description = "CIDR block for the second public subnet."
  type        = string
  default     = "10.0.2.0/24"
}

variable "availability_zone_1" {
  description = "Primary availability zone."
  type        = string
  default     = "us-east-1a"
}

variable "availability_zone_2" {
  description = "Secondary availability zone."
  type        = string
  default     = "us-east-1b"
}

variable "instance_type" {
  description = "EC2 instance type for the API server."
  type        = string
  default     = "t3.micro"
}

variable "app_port" {
  description = "Port exposed by the FastAPI service."
  type        = number
  default     = 8000
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to connect to the EC2 instance over SSH."
  type        = string
  default     = "0.0.0.0/0"
}

variable "key_pair_name" {
  description = "Existing AWS EC2 key pair name to enable SSH access."
  type        = string
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "torneo_db"
}

variable "db_username" {
  description = "PostgreSQL admin username."
  type        = string
  default     = "torneo_user"
}

variable "db_password" {
  description = "PostgreSQL admin password."
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance size."
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Storage size in GiB for the database."
  type        = number
  default     = 20
}
