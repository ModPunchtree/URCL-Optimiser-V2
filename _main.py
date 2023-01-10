
from URCLOptimiserV2.optimiser_main import optimiseURCL
from URCLOptimiserV2.optimisationByEmulation import optimisationByEmulation



f = open("test.urcl", "r")
code = f.read()
f.close()


code, optimisationCount = optimiseURCL(code, maxCycles=500, M0=0, MAXBLOCKSIZE=40, compiled=True)

#BITS = 16
#MINREG = 25
#HEAPTotal = 2**12
#cycleLimit = 100000
#code = optimisationByEmulation(code[5: ], BITS, MINREG, HEAPTotal, cycleLimit)

result = ""
for line in code:
    result += " ".join(line)
    result += "\n"

if result[-1: ] == "\n":
    result = result[: -1]

print(f"\n{result}\n")
