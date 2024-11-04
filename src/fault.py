from enum import Enum

class FaultType(Enum):
    SA_0 = 0
    SA_1 = 1

class fault:
    wire_idx = None
    sa_val: int = -1

    def __init__(self, idx, val):
        self.wire_idx = idx
        self.sa_val = val

    def __str__(self) -> str:
        return f'{self.wire_idx.val} stuck at {self.sa_val}'

    def __eq__(self, other) -> bool:
        return (self.wire_idx == other.wire_idx) and (self.sa_val == other.sa_val)

