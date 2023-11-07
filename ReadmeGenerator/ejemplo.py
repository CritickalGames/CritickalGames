import json
import os
from helpers import types, set_config

FILEPATH = "../"
PATH = "ReadmeGenerator/"
FILENAME_BASE = f"{PATH}config_base.json"
FILENAME_PROJECTS = f"{PATH}config_projects.json"


with open(FILENAME_BASE, 'r', errors="ignore", encoding="utf-8") as f:
    data = json.loads(f.read())
    readme_file = ""
    context = {}

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

    f = open(f"{FILEPATH}{category['tag']}.md", "w", errors="ignore")
    f.write(readme_file)
    f.close()
    
print(readme_file)