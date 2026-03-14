from fastapi import APIRouter, Request
from engine.workflow_engine import WorkflowEngine
from engine.graph import WorkflowGraph, Node

router = APIRouter()

engine = WorkflowEngine()


@router.post("/webhook/{workflow_id}")
async def webhook_trigger(workflow_id: str, request: Request):

    # -----------------------------
    # Safe JSON parsing
    # -----------------------------
    try:
        data = await request.json()
    except:
        data = {}

    # -----------------------------
    # Example workflow graph
    # -----------------------------
    graph = WorkflowGraph()

    graph.add_node(Node("step1", "send_email"))
    graph.add_node(Node("step2", "save_db"))

    # -----------------------------
    # Execute workflow
    # -----------------------------
    try:
        result = engine.run(graph, data)

        return {
            "workflow_id": workflow_id,
            "status": "executed",
            "result": result
        }

    except Exception as e:

        return {
            "workflow_id": workflow_id,
            "status": "failed",
            "error": str(e)
        }