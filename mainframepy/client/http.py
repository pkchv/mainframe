import httpx

from mainframepy.core.exceptions import ServerError
from mainframepy.core.msgpack import pack, unpack


def call(data: dict, host="localhost", port=8080, timeout=300):
    client = httpx.Client(base_url=f"http://{host}:{port}", timeout=timeout)
    headers = {
        "content-type": "application/x-msgpack",
        "user-agent": "mainframe-client",
    }
    response = client.post("/", data=pack(data), headers=headers)
    data = unpack(response.content)

    if "$error" in data:
        raise ServerError(data["$error"])

    return data
