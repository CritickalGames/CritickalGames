import json
from helpers import types, set_config
import os

FILEPATH = "../"
ACTUALPATH = "ReadmeGenerator/"
FILENAME_BASE = f"{ACTUALPATH}config_base.json"
FILENAME_PROJECTS = f"{ACTUALPATH}config_projects.json"

f = open(FILENAME_BASE, "r", errors="ignore", encoding="utf-8")
data = json.loads(f.read())

print(data)