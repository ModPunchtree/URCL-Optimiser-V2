
from URCLOptimiserV2.urcl_optimiser_v2 import *

def optimiseURCL(code):
    uniqueNum = 0

    # initial code cleanup
    code, success = removeComments(code)

    code, success = unifySpaces(code)

    code, success = removeEmptyLines(code)

    code, success = defineMacros(code)

    #code, success = convertBases(code)

    code, success = tokenise(code)
    
    code, success = convertBases(code)

    code, BITS, MINHEAP, MINSTACK, RUN, MINREG, success = fixBITS(code)

    code, success = fixNegativeValues(code, BITS)

    code, success = convertDefinedImmediates(code, BITS, MINHEAP, MINSTACK)

    code, uniqueNum, success = relativesToLabels(code, uniqueNum)

    code, success = standardiseSymbols(code)

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
        
        code, success = inverseBranches(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = pointlessWrites(code, MINREG)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = duplicateLOD(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = propagateMOV(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        ## Pair Optimisations
        code, success = SETBranch(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = LODSTR(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = STRLOD(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = ADDADD(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = SUBSUB(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = INCINC(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = DECDEC(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = ADDSUB(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = ADDINC(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = ADDDEC(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = SUBINC(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = SUBDEC(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = INCDEC(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = SUBADD(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = INCADD(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = DECADD(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = INCSUB(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = DECSUB(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = DECINC(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = MLTMLT(code, BITS)
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
    
    if code[-1: ] not in ([["HLT"]], [["JMP"]], [["RET"]]):
        code.append(["HLT"])

    return code, optimisationCount

