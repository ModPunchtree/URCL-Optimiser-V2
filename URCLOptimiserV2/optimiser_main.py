
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

    code, MINREG, success = reduceRegisters(code)

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
        
        code, MINREG, success = reduceRegisters(code)
        overallSuccess |= success
        
        return code, MINREG, overallSuccess

    overallSuccess = True
    optimisationCount = 0
    while overallSuccess == True:
        overallSuccess = False
        
        code, MINREG, success = loopingCodeCleaner(code, MINREG)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = removeR0(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = removeNOPs(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = shortcutBranches(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = pointlessBranches(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = JMP2Subroutine(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = fullImmediateFolding(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = partialImmediateFolding(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = noImmediateFolding(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = immediatePropagation(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = writeBeforeRead(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = detectOUT(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = inlineBranches(code)
        overallSuccess |= success
        optimisationCount += int(success)

    headers = [
        ["BITS", str(BITS)],
        ["MINREG", str(MINREG)],
        ["MINHEAP", str(MINHEAP)],
        ["MINSTACK", str(MINSTACK)],
        ["RUN", RUN]
        ]
    
    code = headers + code
    
    if code[-1: ] != [["HLT"]]:
        code.append(["HLT"])

    return code, optimisationCount

