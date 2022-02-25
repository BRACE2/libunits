#
# python etc/apidoc.py elle/units/defs.yml  > ../../../docs/api/units.md

import sys
import yaml

with open(sys.argv[-1], "r") as f:
    units = yaml.load(f, Loader=yaml.Loader)
    
    print("# units\n")
    print("<!-- python etc/apidoc.py elle/units/defs.yml  > ../../../docs/api/units.md -->\n")
    print("<table>")
    for k, v in units["units"].items():
        if "symbols" in v:
            print(f"\t<tr><td><code>{k}</code></td><td>{str(v['symbols'])}</td></tr>")
    print("</table>")
