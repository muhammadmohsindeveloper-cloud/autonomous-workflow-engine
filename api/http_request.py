import requests

def run(data):

    url = data.get("url")
    method = data.get("method", "GET")
    payload = data.get("payload", {})

    if not url:
        return {"error": "URL missing"}

    try:
        if method == "POST":
            res = requests.post(url, json=payload)
        else:
            res = requests.get(url)

        return {
            "status": res.status_code,
            "response": res.text[:500]
        }

    except Exception as e:
        return {"error": str(e)}