from fastapi import APIRouter
from core.database import DatabaseManager
from core.logger import get_logger

router = APIRouter()

logger = get_logger("workflows")
db = DatabaseManager(logger)


@router.post("/workflows")
def create_workflow(data: dict):

    name = data.get("name")
    definition = data.get("definition")

    workflow_id = db.create_workflow(name, definition)

    return {
        "workflow_id": workflow_id,
        "status": "created"
    }


@router.get("/workflows")
def list_workflows():

    return db.list_workflows()