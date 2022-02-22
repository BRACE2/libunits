from typing import Generic
class DimensionType(float):  # (Generic[str, int]):
    def __init__(self, *args):
        self.ops = args

    def __mul__(self, other):
        return self.ops + ("__mul__", other)

    def __getitem__(self, *items):
        pass


Length = DimensionType()

Force = DimensionType()
