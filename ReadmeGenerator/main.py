import json
from helpers import types, set_config
import os

#Recuerda dar permisos a tu github actions en "Settings>Actions>General".

#FILEPATH = "../" ya no hace falta; "open" lee apartir de ../ReadmeGenerator
README= "../README.md"#Quita el "../" cuando hagas el commit
ACTUALPATH = "ReadmeGenerator/" #Sin esto, no funciona el "open".
#Pero para el commit quita la variable.
FILENAME_BASE = f"config_base.json"
FILENAME_PROJECTS = f"config_projects.json"

f = open(FILENAME_BASE, "r", errors="ignore", encoding="utf-8")
data = json.loads(f.read())

readme_file = ""
context = {}

for block in data:
    if block["type"]=="config":
        github_user = block["data"]["githubUser"]
        categories = block["data"]["categories"]
        context = set_config(github_user, categories)
        continue
    
    readme_file += types[block["type"]](block["data"], context)
    readme_file += "\n\n"



f = open(f"{README}", "w", errors="ignore", encoding="utf-8")
f.write(readme_file)
f.close()

leeme = readme_file

f = open(FILENAME_PROJECTS, "r", errors="ignore", encoding="utf-8")
data = json.loads(f.read())

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
    
    f = open(f"{category['tag']}.md", "w", errors="ignore", encoding="utf-8")
    f.write(readme_file)
    f.close()

