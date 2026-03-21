import requests

def run(data):
    url = data.get("url")
    method = data.get("method", "GET")

    if not url:
        return {"error": "Missing URL"}

    try:
        if method == "POST":
            res = requests.post(url, json=data.get("payload", {}))
        else:
            res = requests.get(url)

        return {
            "status": res.status_code,
            "data": res.json() if "application/json" in res.headers.get("content-type", "") else res.text
        }

    except Exception as e:
        return {"error": str(e)}