import base64
from io import BytesIO

import numpy as np
from PIL.Image import Image


class BytesEncoder(object):
    @staticmethod
    def serialize(raw: bytes) -> str:
        return base64.b64encode(raw).decode()

    @staticmethod
    def deserialize(serialized: str) -> bytes:
        return base64.b64decode(serialized)


class NumpyEncoder(object):
    @staticmethod
    def serialize(raw: np.ndarray) -> bytes:
        buffer = BytesIO()
        np.save(buffer, raw)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def deserialize(serialized: bytes) -> np.ndarray:
        buffer = BytesIO(serialized)
        return np.load(buffer, allow_pickle=True)


class PillowEncoder(object):
    @staticmethod
    def serialize(raw: Image) -> bytes:
        buffer = BytesIO()
        if not raw.format:
            raw.format = "jpeg"

        raw.save(buffer, raw.format, compression="raw", compression_level=0)
        buffer.seek(0)

        return buffer.getvalue()

    @staticmethod
    def deserialize(serialized: bytes) -> Image:
        buffer = BytesIO(serialized)
        return Image.open(buffer)


encoder_defs = [
    ("ndarray", np.ndarray, NumpyEncoder),
    ("image", Image, PillowEncoder),
]
