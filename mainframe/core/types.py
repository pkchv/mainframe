import numpy as np
from PIL.Image import Image
from pydantic import BeforeValidator, PlainSerializer
from typing_extensions import Annotated

from core.encoders import NumpyEncoder, PillowEncoder

Base64NumpyArrayType = Annotated[
    np.ndarray,
    BeforeValidator(NumpyEncoder.deserialize),
    PlainSerializer(NumpyEncoder.serialize, return_type=str),
]

Base64ImageType = Annotated[
    Image,
    BeforeValidator(PillowEncoder.deserialize),
    PlainSerializer(PillowEncoder.serialize, return_type=str),
]
