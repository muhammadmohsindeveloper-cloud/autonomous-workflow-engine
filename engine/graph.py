from typing import Dict, List


class Node:
    def __init__(self, node_id: str, plugin: str, next_nodes: List[str] = None):
        self.node_id = node_id
        self.plugin = plugin
        self.next_nodes = next_nodes or []


class WorkflowGraph:
    """
    Simple DAG graph for workflows
    """

    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node: Node):
        self.nodes[node.node_id] = node

    def get_node(self, node_id: str):
        return self.nodes.get(node_id)

    def start_nodes(self):
        return list(self.nodes.values())