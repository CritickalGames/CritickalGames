import json
from helpers import types, set_config
import os

# Recuerda dar permisos a tu github actions en "Settings>Actions>General".

README = "README.md"
ACTUALPATH = ".ReadmeGenerator/"  # ! Sin esto, no funciona el "open".
DIRECCION_MD = "md/"  # ! Para direccionar los MD
DIRECCION_JSON = "json/"
# Pero para el commit quita la variable.
FILENAME_BASE = f"{DIRECCION_JSON}config_base.json"
FILENAME_PROJECTS = f"{DIRECCION_JSON}config_projects.json"

# Función para abrir un archivo o crearlo si no existe
def open_or_create_file(filename, mode):
    if not os.path.exists(filename):
        with open(filename, 'w', errors="ignore", encoding="utf-8") as f:
            pass
    return open(filename, mode, errors="ignore", encoding="utf-8")

# Leer configuración base
with open_or_create_file(FILENAME_BASE, "r") as f:
    data = json.loads(f.read())

readme_file = ""
context = {}

# Procesar bloques de configuración
for block in data:
    if block["type"] == "config":
        github_user = block["data"]["githubUser"]
        categories = block["data"]["categories"]
        context = set_config(github_user, categories)
        continue

    readme_file += types[block["type"]](block["data"], context)
    readme_file += "\n\n"

# Escribir en README.md
with open_or_create_file(README, "w+") as f:
    f.write(readme_file)
    f.seek(0)
    print(f.read())

# Leer configuración de proyectos
with open_or_create_file(FILENAME_PROJECTS, "r") as f:
    data = json.loads(f.read())

# Procesar categorías y escribir archivos md
for category in categories:
    readme_file = ""
    temp_context = context.copy()
    temp_context["category"] = category["name"]
    temp_context["emoji"] = category["emoji"]
    temp_context["projects"] = [
        x for x in context["projects"] if category["tag"] in x["tags"]
    ]
    for block in data:
        readme_file += types[block["type"]](block["data"], temp_context)
        readme_file += "\n\n"

    filename_md = f"{DIRECCION_MD}{category['tag']}.md"
    with open_or_create_file(filename_md, "w") as f:
        f.write(readme_file)
