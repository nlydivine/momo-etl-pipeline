import base64

USERNAME = "admin"
PASSWORD = "momo123"


def check_auth(headers):
    """
    Validate Basic Authentication credentials.
    """

    auth_header = headers.get("Authorization")

    if not auth_header:
        return False

    try:
        auth_type, credentials = auth_header.split()

        if auth_type != "Basic":
            return False

        decoded = base64.b64decode(
            credentials
        ).decode("utf-8")

        username, password = decoded.split(":")

        return (
            username == USERNAME
            and password == PASSWORD
        )

    except Exception:
        return False


def send_unauthorized(handler):
    """
    Send a 401 Unauthorized response.
    """

    handler.send_response(401)

    handler.send_header(
        "WWW-Authenticate",
        'Basic realm="MoMo API"'
    )

    handler.end_headers()

    handler.wfile.write(
        b'{"error":"Unauthorized"}'
    )
