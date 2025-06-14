# Paper 2 Code: AI Team
Repositorio del equipo de AI.

## Cómo correr el repositorio
```shell
$ uv sync
$ lightning deploy src/main.py
```

## Cómo probar los endpoints
Una vez desplegado el modelo, ir a `localhost:8000/docs` (documentación Swagger de la API)
el endpoint predict permite pasa un texto en JSON y ese texto será convertido a un archivo .py dentro
 de un .zip.