from pathlib import Path

try:
    import orjson as json

except ImportError:
    import json


__all__ = ["UnitHandler"]

JSON_DIR = Path(__file__).parents[0] / "json/"


def load(system, overrides, abbrev=True):
    abbrev_ext = "-w_abbrev" if abbrev else ""

    def_file = JSON_DIR / f"{system}{abbrev_ext}.json"
    try:
        with open(def_file, "r") as f:
            defs = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Cannot find unit definition file {def_file}")

    # if overrides:
    #    with open(JSON_DIR/"units.json", "r") as f:
    #        all_units = json.load(f)

    # for override in overrides:
    #    dimension = all_units["units"][override]["dimension"]
    #    base = all_units["systems"][system]["base_units"][dimension]
    #    scale = 1/all_units["units"][override]["si"]

    #    for unit in defs:
    #        if all_units["units"][unit]["dimension"] == dimension:
    #            defs[unit] *= scale * all_units["units"][unit]["si"]

    return defs


class SpacedDimensions:
    def __init__(self, step, justification):
        self.justification = justification
        self.step = step

    def __matmul__(self, num):
        assert isinstance(num, int)
        if self.justification in ["c", "centered"]:
            begin = -sum([self.step] * num) / 2

        elif self.justification in ["l", "left"]:
            begin = 0.0

        return [begin + self.step * i for i in range(num + 1)]

    def __rmatmul__(self, num):
        return self.__matmul__(num)


class Dimension(float):
    def __mul__(self, other):
        try:
            out = float.__mul__(self, float(other))
        except:
            out = type(other)(
                [
                    # float mult if scalar, else recurse
                    float.__mul__(self, i) if isinstance(i, (float, int)) else other * i
                    for i in other
                ]
            )
        return out

    def __rmul__(self, other):
        return self * other


class UnitHandler:
    def __init__(self, base, abbrev=True):
        system, *overrides = base.split(", ")
        self.base_dims = load(system, overrides)
        # for key, val in build_conversions(abbrev=abbrev,**base_dims).items():
        #    setattr(self, key, val)

    def __getattr__(self, name):
        return Dimension(self.base_dims[name])

    def __repr__(self):
        return f"""<{', '.join(self.base_dims.keys())}>"""

    def dim(self, dim):
        feet, inches = map(float, dim.split("-"))
        return feet * self.foot + inches * self.inch

    def spacing(self, dim, justification="l"):
        if isinstance(dim, str):
            dim = self.dim(dim)
        return SpacedDimensions(dim, justification)
