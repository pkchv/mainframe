from functools import wraps

from fastapi import FastAPI, Request, Response
from loguru import logger

from core.msgpack import pack, unpack


class MainframeAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, route):
        async def predict_endpoint(request: Request):
            try:
                raw_request_body = await request.body()
                request_data = unpack(raw_request_body)
                _content = await route(**request_data)
                content = pack(_content)
                return Response(content=content, media_type="application/x-msgpack")
            except Exception as e:
                try:
                    logger.error(e, exc_info=True)
                except Exception as _:
                    logger.error(str(e))

                return Response(
                    content=pack({"$error": str(e)}),
                    media_type="application/x-msgpack",
                )

        @wraps(route)
        async def wrapper(*args, **kwargs):
            return await route(*args, **kwargs)

        self.add_api_route("/", predict_endpoint, methods=["POST"])

        return wrapper
