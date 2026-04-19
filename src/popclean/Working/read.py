import sys
import os

f = sys.argv[1]


out = open(f[: f.index(".") + 1] + "py", "w")
file = open(f, "r")
start = True
for line in file:

    line = line[: len(line)]
    templine = line.lstrip()
    if "RealT" in line:
        out.write(line)
    elif ("=" in line and "(" in line and '"' in line) or ("=" in line and "[" in line):
        out.write(line)
    else:
        if "=" in templine and not "==" in templine:
            templine = templine[: templine.index("=") + 1]
        if (
            "." in templine
            and "=" in templine
            and start == True
            and not "==" in templine
            and not "(" in templine
        ):
            if (
                templine.count(".") == 1
                or ".NS." in templine
                or ".comp" in templine
                or ".twoPhase" in templine
                or ".MN" in templine
                or ".FAR" in templine
            ):
                out.write(line[: line.index("=")] + "+" + line[line.index("=") :])
            else:
                out.write(line)
        else:
            out.write(line)

out.close()

os.system("python " + f[: f.index(".") + 1] + "py")
