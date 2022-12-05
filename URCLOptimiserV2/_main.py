
from URCLOptimiserV2.urcl_optimiser_v2 import *

def optimiseURCL(code):
    uniqueNum = 0

    # initial code cleanup
    code, success = removeComments(code)

    code, success = unifySpaces(code)

    code, success = removeEmptyLines(code)

    code, success = defineMacros(code)

    code, success = convertBases(code)

    code, success = tokenise(code)

    code, BITS, MINHEAP, MINSTACK, RUN, MINREG, success = fixBITS(code)

    code, success = fixNegativeValues(code, BITS)

    code, success = convertDefinedImmediates(code, BITS, MINHEAP, MINSTACK)

    code, uniqueNum, success = relativesToLabels(code, uniqueNum)

    code, success = removeUnusedLabels(code)

    code, success = removeMultiLabels(code)

    code, success = moveDWValues(code)

    code, success = removeUnreachableCode(code)

    code, MINREG, success = reduceRegisters(code, MINREG)

    #########################################

    # main optimisations

    def loopingCodeCleaner(code: list, MINREG: int):
        overallSuccess = False
        
        code, success = removeUnusedLabels(code)
        overallSuccess |= success
        
        code, success = removeMultiLabels(code)
        overallSuccess |= success
        
        code, success = removeUnreachableCode(code)
        overallSuccess |= success
        
        code, MINREG, success = reduceRegisters(code, MINREG)
        overallSuccess |= success
        
        return code, MINREG, overallSuccess

    overallSuccess = True
    optimisationCount = 0
    while overallSuccess == True:
        overallSuccess = False
        
        code, MINREG, success = loopingCodeCleaner(code, MINREG)
        overallSuccess |= success
        
        code, success = removeR0(code)
        overallSuccess |= success
        
        code, success = removeNOPs(code)
        overallSuccess |= success

    return code, optimisationCount





f = open("test.urcl", "r")
code = f.read()
f.close()
    
result = ""
for line in code:
    result += " ".join(line)
    result += "\n"

if result[-1] == "\n":
    result = result[: -1]

print(f"\n{result}")

