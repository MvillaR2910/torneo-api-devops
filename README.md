# torneo-api

Proyecto API de futbol con FastAPI y PostgreSQL.

## Infraestructura

La infraestructura de nube para la entrega se encuentra en la carpeta [terraform](./terraform).

Alli se incluyen los archivos `.tf` y la guia basica para desplegar:

- red base en AWS
- instancia EC2 para la API
- base de datos PostgreSQL en RDS
- seguridad para SSH, aplicacion y base de datos

## Despliegue con Terraform

Sigue la guia detallada en [terraform/README.md](./terraform/README.md).
