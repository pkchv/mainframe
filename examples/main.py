import numpy as np

from mainframe.server.api import MainframeAPI

api = MainframeAPI()


@api.predict
async def predict(text: str, arr: np.ndarray):
    return {"arr": np.array([1, 2, 3])}
