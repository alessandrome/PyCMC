from PyCMC.models import APIModel
from dataclasses import dataclass
from typing import Optional


@dataclass
class Status(APIModel):
    timestamp: str
    error_code: int
    error_message: Optional[str] = None
    elapsed: Optional[int] = None
    credit_count: Optional[int] = None
