from plugins.loader import load_plugin
from plugins.sandbox import safe_execute


class NodeExecutor:

    def execute(self, node):
        """
        Execute a single workflow node
        """

        try:
            plugin_name = node.get("type")
            data = node.get("data", {})

            if not plugin_name:
                return {
                    "status": "error",
                    "message": "Missing node type"
                }

            # 🔥 LOAD PLUGIN (WITH RELOAD FIX)
            plugin = load_plugin(plugin_name)

            # handle loader errors
            if isinstance(plugin, dict) and "error" in plugin:
                return {
                    "status": "error",
                    "plugin": plugin_name,
                    "message": plugin["error"]
                }

            # 🔥 EXECUTE
            result = safe_execute(plugin, data)

            # 🔥 NORMALIZE RESULT (IMPORTANT)
            if isinstance(result, dict) and result.get("status") == "error":
                return {
                    "status": "error",
                    "plugin": plugin_name,
                    "message": result.get("message", "Unknown error")
                }

            return {
                "status": "success",
                "plugin": plugin_name,
                "input": data,
                "result": result
            }

        except Exception as e:
            return {
                "status": "error",
                "plugin": node.get("type", "unknown"),
                "message": str(e)
            }