import uuid

class Executor:

    def build_workflow(self, plan: dict):
        """
        Convert plan → workflow JSON
        """

        nodes = []
        edges = []

        previous_id = None

        for step in plan["steps"]:

            node_id = str(uuid.uuid4())

            node = {
                "id": node_id,
                "type": step
            }

            nodes.append(node)

            if previous_id:
                edges.append({
                    "from": previous_id,
                    "to": node_id
                })

            previous_id = node_id

        return {
            "nodes": nodes,
            "edges": edges
        }