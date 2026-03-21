import importlib
import sys


def load_plugin(name: str):
    """
    Dynamically load plugin safely with FORCE reload
    """

    try:
        module_name = f"plugins.{name}"

        # 🔥 FORCE RELOAD (guaranteed fresh code)
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)

        # 🔥 DEBUG (VERY IMPORTANT)
        print(f"🔥 LOADED PLUGIN: {name} FROM -> {module.__file__}")

        # ensure run() exists
        if not hasattr(module, "run"):
            return {
                "error": f"Plugin '{name}' missing run() function"
            }

        return module

    except ModuleNotFoundError:
        return {
            "error": f"Plugin '{name}' not found"
        }

    except Exception as e:
        return {
            "error": str(e)
        }