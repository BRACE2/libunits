# elle.units
# July 2021

import sys
import json
from pathlib import Path
from decimal import Decimal

import yaml

ACCURACIES = list(range(0,10,5))

def dec_prec(accuracy):
    pass

if __name__=="__main__":

    yaml_definitions = sys.argv[1]
    json_directory = Path(sys.argv[2])
    
    abbreviate = True
    abbrev_ext = "-w_abbrev" if abbreviate else "" 

    with open(yaml_definitions, "r") as f:
        defs = yaml.load(f, Loader=yaml.Loader)

    with open(json_directory / "units.json", "w+") as f:
        json.dump(defs, f)

    for group in defs["systems"]:
        conversions = {}
        group_file = json_directory / f"{group}{abbrev_ext}.json"
        base_units = defs["systems"][group]["base_units"]
        for name, unit in defs["units"].items():
            dimension = unit["dimension"]
            if dimension in base_units:
                dest_unit = base_units[dimension]

                #decimal.getcontext().prec = prec
                scale = Decimal(unit["si"]) / Decimal(defs["units"][dest_unit]["si"])
                print(scale)
                conversions[name] = float(scale)

                if abbreviate:
                    for abbrev in unit["symbols"]:
                        conversions[abbrev] = conversions[name]
        conversions["gravity"] = defs["constants"]["gravitational_acceleration"]["si"] / defs["units"][base_units["LENGTH"]]["si"]
        with open(group_file, "w+") as f:
            json.dump(conversions, f)



