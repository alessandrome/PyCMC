from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass
class Hydratable(Generic[T]):
    """
    Wrapper for an optional *hydratable* value. A *hydratable* value is a value that may be omitted or not present
    in an API response. Please note that a `None` value is different from a *not present* (i.e. *not hydrated*) value.
    This is similar to the distinction between `undefined` and `null` in JavaScript.

    This class is useful to distinguish the following cases:
    - The value is not present (`present == False`)
    - The value is present but explicitly set to `None` (`value is None`)
    - The value is present and holds a non-null value

    Useful when parsing data from JSON, forms, databases, or APIs where it is important to know whether a field was present.

    Examples:
        >>> h = Hydratable(value=10, present=True)
        >>> h.unwrap()       # 10
        >>> h + 5            # 15
        >>> bool(h)          # True

        >>> h = Hydratable(value=None, present=True)
        >>> bool(h)          # False
        >>> h.unwrap(default=0)  # Returns None, not 0, because h.present == True

        >>> h = Hydratable(value=None, present=False)
        >>> h.unwrap(default=0)  # Returns 0

    Args:
        value (Optional[T]): The encapsulated value.
        present (bool): Indicates whether the value is present and hydrated (default: False).
    """
    value: Optional[T] = None
    present: bool = False

    def unwrap(self, default: Optional[T] = None) -> Optional[T]:
        return self.value if self.present else default

    def get_value(self) -> Optional[T]:
        if not self.present:
            raise ValueError("Value is not present and hydrated")
        return self.value

    def set_value(self, value: T, present: bool = True) -> None:
        self.value = value
        self.present = present

    def dehydrate(self):
        self.present = False

    def is_present(self) -> bool:
        return self.present

    def is_null(self) -> bool:
        return self.present and self.value is None

    def __bool__(self):
        return self.present and bool(self.value)

    # self.value attributes direct wrapper
    def __getattr__(self, name):
        if not self.present:
            raise AttributeError(f"'{name}' not available: field not hydrated")
        return getattr(self.value, name)

    def __str__(self):
        return str(self.value) if self.present else "<not hydrated>"

    def __repr__(self):
        if self.present:
            return f"Hydratable({repr(self.value)})"
        return "Hydratable(<not hydrated>)"

    def __eq__(self, other):
        return self.value == other if self.present else False

    def __add__(self, other):
        if not self.present:
            raise ValueError("Cannot add: field not hydrated")
        return self.value + other

    def __sub__(self, other):
        if not self.present:
            raise ValueError("Cannot sub: field not hydrated")
        return self.value - other

    def __mul__(self, other):
        if not self.present:
            raise ValueError("Cannot multiply: field not hydrated")
        return self.value * other

    def __truediv__(self, other):
        if not self.present:
            raise ValueError("Cannot divide: field not hydrated")
        return self.value / other

    def __floordiv__(self, other):
        if not self.present:
            raise ValueError("Cannot divide: field not hydrated")
        return self.value // other

    def __lt__(self, other):
        if not self.present:
            raise ValueError("Cannot < compare: field not hydrated")
        return self.value < other

    def __le__(self, other):
        if not self.present:
            raise ValueError("Cannot <= compare: field not hydrated")
        return self.value <= other

    def __gt__(self, other):
        if not self.present:
            raise ValueError("Cannot > compare: field not hydrated")
        return self.value > other

    def __ge__(self, other):
        if not self.present:
            raise ValueError("Cannot >= compare: field not hydrated")
        return self.value >= other
