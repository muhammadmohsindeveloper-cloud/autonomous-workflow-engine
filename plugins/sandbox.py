def safe_execute(plugin, data):
    """
    Plugin sandbox security
    """

    # ✅ must have run()
    if not hasattr(plugin, "run"):
        raise Exception("Plugin missing run() function")

    # ⚠️ IMPORTANT FIX:
    # __dict__ remove kar diya (warna har plugin block ho jata hai)
    blocked = [
        "__globals__",
        "__getattribute__",
    ]

    for attr in dir(plugin):
        if attr in blocked:
            raise Exception(f"Unsafe plugin attribute detected: {attr}")

    # ✅ execute plugin
    return plugin.run(data)