import msgpack

from mainframepy.core.encoders import encoder_defs


def _encode(data):
    for name, data_type, encoder in encoder_defs:
        if isinstance(data, data_type):
            return {"$type": name, "$data": encoder.serialize(data)}

    return data


def _decode(data):
    for name, _, encoder in encoder_defs:
        if data.get("$type") == name:
            return encoder.deserialize(data.get("$data"))

    return data


def pack(data: dict):
    return msgpack.packb(data, default=_encode, use_bin_type=True)


def unpack(packed: bytes):
    return msgpack.unpackb(packed, object_hook=_decode, raw=False)
