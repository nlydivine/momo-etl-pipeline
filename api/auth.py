import base64

USERNAME = "admin"
PASSWORD = "password"


def check_auth(headers):
    auth = headers.get("Authorization")

    if not auth:
        return False

    if not auth.startswith("Basic "):
        return False

    try:
        encoded = auth.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")

        username, password = decoded.split(":")

        return username == USERNAME and password == PASSWORD

    except:
        return False
