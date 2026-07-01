import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(BASE_DIR, "data", "shl_catalog.json")

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)


def find_assessment(name):
    name = name.lower().strip()

    for item in catalog:
        if name == item["name"].lower():
            return item

    for item in catalog:
        if name in item["name"].lower():
            return item

    return None