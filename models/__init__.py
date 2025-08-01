from dataclasses import dataclass, fields, is_dataclass
from typing import get_origin, get_args, Union
from decimal import Decimal
from datetime import datetime


@dataclass
class APIModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_api_response(cls, json_data: dict):
        init_data = {}

        for field in fields(cls):
            field_name = field.name
            field_type = field.type
            value = json_data.get(field_name)

            if value is None:
                init_data[field_name] = None
                continue

            origin = get_origin(field_type)
            args = get_args(field_type)

            # --- Optional[...] ---
            if origin is Union and type(None) in args:
                actual_type = [a for a in args if a is not type(None)][0]
                value = cls._parse_value(actual_type, value)

            # --- List[...] ---
            elif origin is list:
                item_type = args[0]
                if isinstance(value, list):
                    value = [cls._parse_value(item_type, v) for v in value]

            # --- Direct object ---
            else:
                value = cls._parse_value(field_type, value)

            init_data[field_name] = value

        return cls(**init_data)

    @staticmethod
    def _parse_value(field_type, value):
        if isinstance(field_type, type):
            if issubclass(field_type, APIModel) and isinstance(value, dict):
                return field_type.from_api_response(value)

            elif is_dataclass(field_type) and isinstance(value, dict):
                return field_type(**value)

            elif field_type is Decimal:
                return Decimal(str(value))  # Safe conversion from str/int/float

            elif field_type is datetime:
                return datetime.fromisoformat(value)  # Assumes ISO 8601

        return value
