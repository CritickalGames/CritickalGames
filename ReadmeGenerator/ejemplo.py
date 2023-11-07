import json
import os
from helpers import types, set_config

FILEPATH = "../"
PATH = "ReadmeGenerator/"
FILENAME_BASE = f"{PATH}config_base.json"
FILENAME_PROJECTS = f"{PATH}config_projects.json"

with open(FILENAME_BASE, 'r', errors="ignore", encoding="utf-8") as arch:
    f = arch.read()
    data = json.loads(f)
    readme_file = ""
    context = {}

try:
    for block in data:
        if block["type"] == "config":
            github_user = block["data"]["githubUser"]
            categories = block["data"]["categories"]
            context = set_config(github_user, categories)
            continue

    readme_file += types[block["type"]](block["data"], context)
    readme_file += "\n\n"

    with open(f"{FILEPATH}README.md", "w", errors="ignore", encoding="utf-8") as f:
        f.write(readme_file)
        f.close()
except TypeError as e:
    print("Supongo que se desbordó: ")
    print(e)

try:
    for category in categories:
        readme_file = ""
        temp_context = context.copy()
        temp_context["categories"] = category["name"]
        temp_context["categories_emoji"] = category["emoji"]
        temp_context["projects"] = [
            x for x in context["projects"] if category["tag"] in x["tags"]
        ]
    
        for block in data:
            readme_file += types[block["type"]](block["data"], temp_context)
            readme_file += "\n\n"
        with open(f"{FILEPATH}{category['tag']}.md", "w", errors="ignore") as f:
            f.write(readme_file)
            f.close()

except:
    print("Supongo que se desbordó")

    print(readme_file)