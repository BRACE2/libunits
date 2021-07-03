from pathlib import Path

import yaml

__all__ = ["UnitHandler"]

DEF_FILE = Path(__file__).parents[0]/"defs.yml"

class SpacedDimensions:
    def __init__(self, step, justification):
        self.justification = justification
        self.step  = step

    def __matmul__(self, num):
        assert isinstance(num, int)
        if self.justification in ["c", "centered"]:
            begin = -sum([self.step]*num)/2

        elif self.justification in ["l", "left"]:
            begin = 0.0

        return [begin + self.step*i for i in range(num+1)]

    def __rmatmul__(self, num):
        return self.__matmul__(num)


class Dimension(float):
    def __mul__(self, other):
        try:
            out = float.__mul__(self, float(other))
        except:
            out = type(other)([
                # float mult if scalar, else recurse
                float.__mul__(self, i) if isinstance(i, (float, int)) else other*i 
                    for i in other 
            ])
        return out

    def __rmul__(self, other):
        return self * other


def build_conversions(abbrev=True,**kwds)->dict:
    with open(DEF_FILE, "r") as f:
        defs = yaml.load(f, Loader=yaml.Loader)
    output = {}
    for name,unit in defs.items():
        if "dimension" in unit and unit["dimension"] in kwds:
            dimension = unit["dimension"]
            dest_unit = kwds[dimension]
            output[name] = Dimension(unit["si"] / defs[dest_unit]["si"])
            if abbrev:
                for abbrev in unit["abbrev"]:
                    output[abbrev] = output[name]
    return output

def get_bases(base):
    with open(DEF_FILE, "r") as f:
        defs = yaml.load(f, Loader=yaml.Loader)
    return defs["_groups"][base]


class UnitHandler:
    def __init__(self, base, abbrev=True):
        self.base_dims = base_dims = get_bases(base)    
        for key, val in build_conversions(abbrev=abbrev,**base_dims).items():
            setattr(self, key, val)


    def __repr__(self):
        return f"""<{', '.join(self.base_dims.values())}>"""

    def dim(self, dim):
        feet, inches = map(float,dim.split("-"))
        return feet * self.foot + inches * self.inch

    def spacing(self, dim, justification="l"):
        if isinstance(dim,str):
            dim = self.dim(dim)
        return SpacedDimensions(dim, justification)

