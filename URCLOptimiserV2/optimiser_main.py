
from URCLOptimiserV2.urcl_optimiser_v2 import *

def optimiseURCL(code, maxCycles = 500, M0 = -1):
    uniqueNum = 0

    # initial code cleanup
    code, success = removeComments(code)

    code, success = unifySpaces(code)

    code, success = removeEmptyLines(code)

    code, success = defineMacros(code)

    code, success = tokenise(code)
    
    # append HLT to prevent floating labels at end of input
    code.append(["HLT"])
    
    code, success = convertBases(code)

    code, BITS, MINHEAP, MINSTACK, RUN, MINREG, success = fixBITS(code)

    code, success = fixNegativeValues(code, BITS)

    code, success = convertDefinedImmediates(code, BITS, MINHEAP, MINSTACK)

    code, success = DWArraytoSingle(code)

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

    # append HLT if it doesn't exist
    if code[-1: ] not in ([["HLT"]], [["JMP"]], [["RET"]]):
        code.append(["HLT"])

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
        
        #code, success = detectOUT(code)
        #overallSuccess |= success
        #optimisationCount += int(success)
        
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
        
        code, success = fixMOVIMM(code)
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
        
        code, success = DIVDIV(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = LSHLSH(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = RSHRSH(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = SRSSRS(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSLBSL(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSRBSR(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSSBSS(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = LSHBSL(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSLLSH(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = RSHBSR(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSRRSH(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = SRSBSS(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSSSRS(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = RSHSRS(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = RSHBSS(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = LSHRSH(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = RSHLSH(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSLBSR(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = BSRBSL(code, BITS)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = ANDAND(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = XORXOR(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        code, success = PSHPOP(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        # aggressive inliner
        code, success = inliner(code)
        overallSuccess |= success
        optimisationCount += int(success)
        
        ## Optimisation By Emulation
        code, success = OBE(code, BITS, MINREG, MINHEAP, maxCycles, M0)
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

def debugPrint(code: list):
    result = ""
    for line in code:
        result += " ".join(line)
        result += "\n"

    if result[-1: ] == "\n":
        result = result[: -1]
    
    return result
