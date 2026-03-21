print("🔥 SEND_EMAIL LOADED")

def run(data):
    print("🔥 SEND_EMAIL RUN CALLED")

    message = data.get("data") or data

    return {
        "email": "sent",
        "message": message
    }