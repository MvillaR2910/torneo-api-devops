# torneo-api

API de futbol construida con FastAPI y PostgreSQL. Este proyecto fue desplegado en AWS usando Terraform, con una instancia EC2 para la aplicacion y una base de datos PostgreSQL en RDS.

## Contenido

- API FastAPI para equipos, jugadores, partidos, integracion y metricas
- Infraestructura en AWS creada con Terraform
- Scripts SQL para crear tablas, insertar y consultar datos, y eliminar tablas
- Flujo de prueba por SSH para conectarse a la base de datos y ejecutar scripts manualmente

## Estructura general

```text
app/                 codigo fuente de la API
tests/               pruebas automatizadas
terraform/           infraestructura en AWS con Terraform
scripts_db/          scripts SQL para la base de datos
Dockerfile           imagen de la API
docker-compose.yml   apoyo local para desarrollo
requirements.txt     dependencias Python
```

## Requisitos previos

Antes de ejecutar el proyecto en AWS se necesita:

1. Tener Python y dependencias para trabajar localmente.
2. Tener Docker instalado localmente si se desea probar con contenedor.
3. Tener Terraform instalado.
4. Tener AWS CLI instalado.
5. Tener una cuenta de AWS con permisos para crear:
   VPC, subnets, internet gateway, route tables, security groups, EC2 y RDS.
6. Tener un key pair creado en AWS para entrar por SSH a la EC2.

## Infraestructura en AWS

La infraestructura se encuentra en la carpeta [terraform](./terraform).

### Recursos creados

- 1 VPC
- 2 subnets publicas
- 1 internet gateway
- 1 route table publica
- 1 security group para la EC2
- 1 security group para RDS
- 1 instancia EC2 para correr la API
- 1 instancia RDS PostgreSQL
- 1 DB subnet group

### Archivos importantes de Terraform

- [terraform/provider.tf](./terraform/provider.tf)
- [terraform/variables.tf](./terraform/variables.tf)
- [terraform/vpc.tf](./terraform/vpc.tf)
- [terraform/network.tf](./terraform/network.tf)
- [terraform/security_groups.tf](./terraform/security_groups.tf)
- [terraform/ec2.tf](./terraform/ec2.tf)
- [terraform/rds.tf](./terraform/rds.tf)
- [terraform/outputs.tf](./terraform/outputs.tf)
- [terraform/terraform.tfvars.example](./terraform/terraform.tfvars.example)

## Configuracion inicial de AWS

### 1. Configurar AWS CLI

En PowerShell local:

```powershell
aws configure
```

Valores usados:

- `AWS Access Key ID`: credencial IAM
- `AWS Secret Access Key`: credencial IAM
- `Default region name`: `us-east-1`
- `Default output format`: `json`

Validar configuracion:

```powershell
aws sts get-caller-identity
```

### 2. Crear el key pair

En la consola de AWS:

1. Ir a `EC2`
2. Entrar a `Key Pairs`
3. Crear uno nuevo, por ejemplo `torneo-api-key`
4. Descargar el archivo `.pem`

Ese nombre debe coincidir con `key_pair_name` en `terraform.tfvars`.

## Preparar variables de Terraform

Desde la carpeta `terraform`, copiar el archivo de ejemplo:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Editar `terraform.tfvars` y llenar al menos:

```hcl
project_name     = "torneo-api"
aws_region       = "us-east-1"
key_pair_name    = "torneo-api-key"
allowed_ssh_cidr = "0.0.0.0/0"
db_password      = "tu_password"
app_port         = 8000
```

## Desplegar la infraestructura

Todo esto se ejecuta en la terminal local del PC, no dentro de la EC2.

```powershell
cd C:\Users\Mateo\Documents\torneo-api\terraform
terraform init
terraform plan
terraform apply
```

Cuando Terraform solicite confirmacion, escribir:

```text
yes
```

Al finalizar, Terraform mostrara algo similar a:

```text
ec2_public_dns = "ec2-xx-xx-xx-xx.compute-1.amazonaws.com"
ec2_public_ip = "xx.xx.xx.xx"
rds_endpoint = "torneo-api-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432"
ssh_command = "ssh -i <your-key>.pem ec2-user@xx.xx.xx.xx"
```

## Entrar por SSH a la EC2

Este comando se ejecuta en PowerShell local:

```powershell
ssh -i "C:\ruta\torneo-api-key.pem" ec2-user@EC2_PUBLIC_IP
```

Ejemplo:

```powershell
ssh -i "C:\Users\Mateo\Documents\necesarios-terraform\torneo-api-key.pem" ec2-user@32.192.2.105
```

La primera vez SSH pedira confirmacion del host:

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Se debe responder:

```text
yes
```

Una vez conectado, el prompt cambia a algo como:

```bash
[ec2-user@ip-10-0-1-61 ~]$
```

## Subir el proyecto a la EC2

Dentro de la consola SSH de la EC2:

```bash
git clone -b feature/api-v2 https://github.com/MvillaR2910/torneo-api-devops.git
cd torneo-api-devops
git status
```

## Configurar variables de entorno en la EC2

Dentro de la carpeta del proyecto en la EC2:

```bash
nano .env
```

Contenido usado:

```env
DATABASE_URL=postgresql://torneo_user:TU_PASSWORD@torneo-api-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432/torneo_db
DATABASE_URL_TEST=postgresql://torneo_test_user:torneo_test_pass@localhost:5433/torneo_test_db
```

Reemplazar `TU_PASSWORD` por el valor real de `db_password` usado en `terraform.tfvars`.

Guardar con:

- `Ctrl + O`
- `Enter`
- `Ctrl + X`

## Levantar la API en AWS

Dentro de la EC2, en la carpeta del proyecto:

```bash
docker build -t torneo-api .
```

Para correr en primer plano:

```bash
docker run --env-file .env -p 8000:8000 --name torneo-api-container torneo-api
```

Para dejar la aplicacion corriendo en segundo plano:

```bash
docker rm -f torneo-api-container
docker run -d --env-file .env -p 8000:8000 --name torneo-api-container torneo-api
```

Verificar contenedor activo:

```bash
docker ps
```

## Probar la API publica

Desde el navegador del PC:

```text
http://EC2_PUBLIC_IP:8000/docs
```

Ejemplo:

```text
http://32.192.2.105:8000/docs
```

Con esto se valida que la API esta desplegada y accesible desde internet.

## Instalar cliente PostgreSQL en la EC2

Dentro de la EC2:

```bash
sudo dnf install -y postgresql15
```

## Conectarse manualmente a RDS desde la EC2

Este paso demuestra que la base de datos se administra remotamente usando SSH hacia la EC2 y desde alli acceso a RDS.

Dentro de la EC2:

```bash
psql "postgresql://torneo_user:TU_PASSWORD@torneo-api-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432/torneo_db"
```

Si la conexion es correcta aparecera:

```text
torneo_db=>
```

Para salir:

```sql
\q
```

## Scripts SQL incluidos

Se agregaron tres scripts en [scripts_db](./scripts_db):

- [scripts_db/01_create_tables.sql](./scripts_db/01_create_tables.sql)
- [scripts_db/02_seed_and_select.sql](./scripts_db/02_seed_and_select.sql)
- [scripts_db/03_drop_tables.sql](./scripts_db/03_drop_tables.sql)

### 1. Crear tablas

```bash
psql "postgresql://torneo_user:TU_PASSWORD@torneo-api-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432/torneo_db" -f scripts_db/01_create_tables.sql
```

### 2. Insertar y consultar datos

```bash
psql "postgresql://torneo_user:TU_PASSWORD@torneo-api-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432/torneo_db" -f scripts_db/02_seed_and_select.sql
```

Este script:

- inserta equipos
- inserta jugadores
- inserta un partido
- inserta una integracion de ejemplo
- ejecuta `SELECT *` sobre las tablas

### 3. Eliminar tablas

```bash
psql "postgresql://torneo_user:TU_PASSWORD@torneo-api-postgres.xxxxx.us-east-1.rds.amazonaws.com:5432/torneo_db" -f scripts_db/03_drop_tables.sql
```

### Flujo recomendado de demostracion

Si la API ya habia creado las tablas, el script de creacion mostrara mensajes de que ya existen. Eso es normal porque la aplicacion usa SQLAlchemy para crear tablas al iniciar.

Para una demostracion limpia se recomienda:

1. correr el script de drop
2. correr el script de create
3. correr el script de seed y select

## Actualizar la EC2 con nuevos cambios

### En el PC local

```powershell
git add .
git commit -m ":sparkles: describe el cambio"
git push origin feature/api-v2
```

### En la EC2

```bash
cd ~/torneo-api-devops
git pull origin feature/api-v2
```

## Versionado semantico y release

Para la entrega se uso versionado semantico.

Ejemplo para crear un tag:

```powershell
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0
```

Luego en GitHub:

1. entrar al repositorio
2. abrir `Releases`
3. seleccionar `Draft a new release`
4. escoger el tag `v2.1.0`
5. publicar el release

## Destruir la infraestructura al terminar

Este es el metodo para eliminar la infraestructura al final de la sustentacion y evitar costos.

Se ejecuta en la terminal local del PC:

```powershell
cd C:\Users\Mateo\Documents\torneo-api\terraform
terraform init
terraform destroy
```

Cuando Terraform pida confirmacion:

```text
yes
```

## Evidencia sugerida para la entrega

- salida de `terraform apply`
- acceso por `SSH` a la EC2
- Swagger en `http://IP_PUBLICA:8000/docs`
- conexion `psql` a RDS desde la EC2
- ejecucion de `01_create_tables.sql`
- ejecucion de `02_seed_and_select.sql`
- ejecucion de `03_drop_tables.sql`
- salida de `terraform destroy`

## Notas finales

- La API corre en Docker dentro de la EC2.
- La base de datos esta en RDS y no se expone publicamente.
- La administracion de la base se hace entrando primero por SSH a la EC2.
- El endpoint publico de la API se consulta por el puerto `8000`.
