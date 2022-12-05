
from URCLOptimiserV2.optimiser_main import optimiseURCL



f = open("test.urcl", "r")
code = f.read()
f.close()


code, optimisationCount = optimiseURCL(code)


result = ""
for line in code:
    result += " ".join(line)
    result += "\n"

if result[-1] == "\n":
    result = result[: -1]

print(f"\n{result}\n")
