from __future__ import annotations
import json
from typing import Dict, ByteString

class DeserializerError(Exception):
    pass


def string_deserializer(data: ByteString, unicode: str = "utf-8", errors: str = "strict") -> str:
    return data.decode(encoding=unicode, errors=errors)


def json_deserializer(data: ByteString, unicode: str = "utf-8") -> Dict:
    try:
        return json.loads(string_deserializer(data, unicode=unicode))
    except json.decoder.JSONDecodeError as exp:
        raise DeserializerError("Bad JSON") from exp

