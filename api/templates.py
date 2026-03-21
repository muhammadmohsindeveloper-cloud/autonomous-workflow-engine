from fastapi import APIRouter
import os, json

router = APIRouter()

TEMPLATE_DIR = "templates"

@router.get("/templates")
def get_templates():

    templates = []

    for file in os.listdir(TEMPLATE_DIR):
        if file.endswith(".json"):
            with open(os.path.join(TEMPLATE_DIR, file), encoding="utf-8") as f:
                templates.append(json.load(f))

    return {"templates": templates}