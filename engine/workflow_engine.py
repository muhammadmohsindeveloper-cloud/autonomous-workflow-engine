from engine.node_executor import NodeExecutor


class WorkflowEngine:

    def __init__(self):
        self.executor = NodeExecutor()

    def run(self, graph, data):
        """
        Execute workflow graph
        """

        results = {}

        for node in graph.nodes.values():

            result = self.executor.execute(node, data)

            results[node.node_id] = result

        return results