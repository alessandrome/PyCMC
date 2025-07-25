from typing import Optional

from PyCMC.models.status import Status


class Result:
    status: Status
    data: Optional[object|list]

    def __init__(self, status: Status, data: Optional[object]):
        self.status = status
        self.data = data

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.status}>"