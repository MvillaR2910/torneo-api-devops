output "ec2_public_ip" {
  description = "Public IP of the API EC2 instance."
  value       = aws_instance.api.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the API EC2 instance."
  value       = aws_instance.api.public_dns
}

output "rds_endpoint" {
  description = "Internal endpoint of the PostgreSQL database."
  value       = aws_db_instance.postgres.endpoint
}

output "ssh_command" {
  description = "Example SSH command once the EC2 instance is running."
  value       = "ssh -i <your-key>.pem ec2-user@${aws_instance.api.public_ip}"
}
