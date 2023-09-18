from __future__ import annotations
import json
from typing import Dict


def string_serializer(data: str, unicode: str = "utf-8"):
    return data.encode(unicode)


def json_serializer(data: Dict, unicode: str = "utf-8"):
    return string_serializer(json.dumps(data), unicode)

