import importlib


def load_plugin(name: str):
    """
    Dynamically load plugins
    """

    module = importlib.import_module(f"plugins.{name}")

    return module