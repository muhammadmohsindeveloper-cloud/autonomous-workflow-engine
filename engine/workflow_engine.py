from engine.node_executor import NodeExecutor


class WorkflowEngine:

    def __init__(self, db=None):
        self.executor = NodeExecutor()
        self.db = db

    def run(self, workflow, input_data=None, workflow_run_id=None):

        nodes = workflow.get("nodes", [])
        edges = workflow.get("edges", [])

        if not nodes:
            return {"error": "No nodes in workflow"}

        graph = {}
        for edge in edges:
            graph.setdefault(edge["from"], []).append(edge["to"])

        all_to = {e["to"] for e in edges}
        start_nodes = [n for n in nodes if n["id"] not in all_to]

        results = {}
        visited = set()

        def execute_node(node_id, data):

            if node_id in visited:
                return

            node = next((n for n in nodes if n["id"] == node_id), None)
            if not node:
                return

            visited.add(node_id)

            merged_data = {}

            if isinstance(data, dict):
                merged_data.update(data)

            if node.get("data"):
                merged_data.update(node["data"])

            # 🔥 LOG BEFORE
            if self.db and workflow_run_id:
                self.db.create_node_run(
                    workflow_run_id,
                    node_id,
                    "running",
                    merged_data,
                    {}
                )

            # 🔥 EXECUTE
            result = self.executor.execute({
                "type": node["type"],
                "data": merged_data
            })

            results[node_id] = result

            # 🔥 LOG AFTER
            if self.db and workflow_run_id:
                status = "success" if result.get("status") == "success" else "error"

                self.db.create_node_run(
                    workflow_run_id,
                    node_id,
                    status,
                    merged_data,
                    result
                )

            # 🔥 CLEAN DATA FLOW
            next_input = {}

            if isinstance(result, dict):
                if result.get("status") == "success":
                    next_input = result.get("result", {})
                else:
                    next_input = {"error": result.get("message")}
            else:
                next_input = result

            for nxt in graph.get(node_id, []):
                execute_node(nxt, next_input)

        for start in start_nodes:
            execute_node(start["id"], input_data or {})

        return {
            "status": "completed",
            "results": results
        }