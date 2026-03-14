from plugins.loader import load_plugin
from plugins.sandbox import safe_execute


class NodeExecutor:

    def execute(self, node, data):
        """
        Execute a single workflow node
        """

        plugin = load_plugin(node.plugin)

        result = safe_execute(plugin, data)

        return result