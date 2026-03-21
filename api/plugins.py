from fastapi import APIRouter
import json
import os

router = APIRouter()

PLUGIN_FILE = os.path.join("marketplace", "plugins.json")


# ✅ LOAD FILE SAFE (UTF-8 FIX)
def load_plugins():
    with open(PLUGIN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ✅ GET ALL PLUGINS
@router.get("/plugins")
def list_plugins():
    try:
        data = load_plugins()
        return data

    except Exception as e:
        return {
            "plugins": [],
            "error": str(e)
        }


# ✅ GET BY CATEGORY (SAFE)
@router.get("/plugins/{category}")
def plugins_by_category(category: str):
    try:
        data = load_plugins()

        filtered = [
            p for p in data.get("plugins", [])
            if p.get("category", "").lower() == category.lower()
        ]

        return {
            "plugins": filtered,
            "count": len(filtered)
        }

    except Exception as e:
        return {
            "plugins": [],
            "error": str(e)
        }