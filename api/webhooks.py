from fastapi import APIRouter, Request
from engine.workflow_engine import WorkflowEngine
from core.database import DatabaseManager
from core.logger import get_logger
import json

router = APIRouter()

logger = get_logger("webhook")
db = DatabaseManager(logger)


@router.post("/webhook/{workflow_id}")
async def webhook_trigger(workflow_id: int, request: Request):

    try:
        data = await request.json()
    except:
        data = {}

    # 🔥 LOAD WORKFLOW
    try:
        with db._connect() as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT definition FROM workflows WHERE id=%s",
                (workflow_id,)
            )

            row = cur.fetchone()
            cur.close()

            if not row:
                return {
                    "workflow_id": workflow_id,
                    "status": "not_found"
                }

            workflow = row[0]

            if isinstance(workflow, str):
                workflow = json.loads(workflow)

    except Exception as e:
        return {
            "workflow_id": workflow_id,
            "status": "db_error",
            "error": str(e)
        }

    # 🔥 CREATE RUN LOG
    run_id = db.create_workflow_run(workflow_id, data)

    try:
        engine = WorkflowEngine(db)

        result = engine.run(
            workflow,
            data,
            workflow_run_id=run_id
        )

        # 🔥 FINAL UPDATE
        db.update_workflow_run(run_id, "completed", result)

        return {
            "workflow_id": workflow_id,
            "run_id": run_id,
            "status": "executed",
            "result": result
        }

    except Exception as e:

        db.update_workflow_run(run_id, "failed", {"error": str(e)})

        return {
            "workflow_id": workflow_id,
            "run_id": run_id,
            "status": "failed",
            "error": str(e)
        }