from fastapi import APIRouter
from core.database import DatabaseManager
from core.logger import get_logger

router = APIRouter()

logger = get_logger("workflows")
db = DatabaseManager(logger)


@router.post("/workflows")
def create_workflow(data: dict):

    name = data.get("name", "Untitled Workflow")
    definition = data.get("definition")

    if not definition:
        return {
            "status": "error",
            "message": "Missing workflow definition"
        }

    try:
        workflow_id = db.create_workflow(name, definition)

        return {
            "id": workflow_id,
            "status": "created"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/workflows")
def list_workflows():

    try:
        workflows = db.list_workflows()

        return {
            "status": "success",
            "count": len(workflows),
            "workflows": workflows
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }