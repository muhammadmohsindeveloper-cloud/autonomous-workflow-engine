def safe_execute(plugin, data):
    """
    Plugin sandbox security
    """

    # Plugin must have execute method
    if not hasattr(plugin, "execute"):
        raise Exception("Plugin missing execute method")

    # Block dangerous attributes
    blocked = [
        "__dict__",
        "__class__",
        "__globals__",
        "__getattribute__",
    ]

    for attr in dir(plugin):

        if attr in blocked:
            raise Exception(
                f"Unsafe plugin attribute detected: {attr}"
            )

    return plugin.execute(data)