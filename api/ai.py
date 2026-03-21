from fastapi import APIRouter
from pydantic import BaseModel

from agent.planner import Planner
from agent.executor import Executor

import requests

router = APIRouter()

planner = Planner()
executor = Executor()


class AIRequest(BaseModel):
    prompt: str


@router.post("/ai/execute")
def run_ai(request: AIRequest):

    try:
        # STEP 1: Plan
        plan = planner.create_plan(request.prompt)

        # STEP 2: Build workflow
        workflow = executor.build_workflow(plan)

        # STEP 3: Save workflow
        save_response = requests.post(
            "http://127.0.0.1:8000/workflows",
            json={
                "name": "AI generated workflow",
                "definition": workflow
            }
        )

        save_res = save_response.json()

        print("SAVE RESPONSE:", save_res)  # DEBUG

        # SAFE extraction
        workflow_id = save_res.get("id") or save_res.get("workflow_id")

        if not workflow_id:
            return {
                "error": "Workflow save failed",
                "save_response": save_res
            }

        # STEP 4: Execute workflow
        run_response = requests.post(
            f"http://127.0.0.1:8000/webhook/{workflow_id}",
            json={}
        )

        run_res = run_response.json()

        return {
            "plan": plan,
            "workflow_id": workflow_id,
            "execution_result": run_res
        }

    except Exception as e:
        return {
            "error": str(e)
        }