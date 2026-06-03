# Terraform

La guia detallada de despliegue, conexion por SSH, ejecucion de scripts SQL y destruccion de infraestructura se encuentra en el [README principal](../README.md).

## Archivos de Terraform

- `provider.tf`: proveedor AWS y version de Terraform
- `variables.tf`: variables del despliegue
- `vpc.tf`: VPC principal
- `network.tf`: subnets, internet gateway y route table
- `security_groups.tf`: reglas para EC2 y RDS
- `ec2.tf`: instancia EC2 para la API
- `rds.tf`: base de datos PostgreSQL en RDS
- `outputs.tf`: IP publica, DNS y endpoint de la base
- `terraform.tfvars.example`: ejemplo de variables

## Flujo rapido

Desde la carpeta `terraform`:

```powershell
terraform init
terraform plan
terraform apply
```

Al terminar la sustentacion:

```powershell
terraform destroy
```
