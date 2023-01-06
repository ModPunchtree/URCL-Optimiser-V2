
from SYL_Compiler.generateURCL_Lib import binaryOperator
from SYL_Compiler.generateURCL_Lib import unaryOperator
from copy import deepcopy

def generateURCL(code: list, varNames: list, funcNames: list, arrNames: list, funcMapNames: list, funcMapLocations: list, BITS: int, MINREG: int, variableTypes: list, functionTypes: list, arrayTypes: list, arrayLengths: list):
    
    funcNames.insert(0, ("global", 0, tuple([]), tuple([])))
    functionTypes.insert(0, ["void"])
    
    varTypes = (
        "int",
        "uint",
        "char",
        "int*",
        "uint*",
        "char*",
        "void",
        "bool",
        "bool*",
        "constint",
        "constuint",
        "constchar",
        "constint*",
        "constuint*",
        "constchar*",
        "constvoid",
        "constbool",
        "constbool*"
    )
    
    funcTypes = (
        "intFunc",
        "uintFunc",
        "charFunc",
        "int*Func",
        "uint*Func",
        "char*Func",
        "voidFunc",
        "boolFunc",
        "bool*Func",
        "constintFunc",
        "constuintFunc",
        "constcharFunc",
        "constint*Func",
        "constuint*Func",
        "constchar*Func",
        "constvoidFunc",
        "constboolFunc",
        "constbool*Func"
    )
    
    arrTypes = (
        "intArr",
        "uintArr",
        "charArr",
        "int*Arr",
        "uint*Arr",
        "char*Arr",
        "voidArr",
        "boolArr",
        "bool*Arr",
        "constintArr",
        "constuintArr",
        "constcharArr",
        "constint*Arr",
        "constuint*Arr",
        "constchar*Arr",
        "constvoidArr",
        "constboolArr",
        "constbool*Arr"
    )
    
    binaryOperators = (
        "%",
        "/",
        "BINARY*",
        "BINARY-",
        "BINARY+",
        ">>",
        "<<",
        ">=",
        ">",
        "<=",
        "<",
        "!=",
        "==",
        "BINARY&",
        "^",
        "|",
        "&&",
        "||"
    )
    
    unaryOperators = (
        "TYPECASTint",
        "TYPECASTuint",
        "TYPECASTchar",
        "TYPECASTint*",
        "TYPECASTuint*",
        "TYPECASTchar*",
        "TYPECASTvoid",
        "TYPECASTbool",
        "TYPECASTbool*",
        "TYPECASTconstint",
        "TYPECASTconstuint",
        "TYPECASTconstchar",
        "TYPECASTconstint*",
        "TYPECASTconstuint*",
        "TYPECASTconstchar*",
        "TYPECASTconstvoid",
        "TYPECASTconstbool",
        "TYPECASTconstbool*",
        
        "sizeof",
        "UNARY*",
        "UNARY+",
        "UNARY-",
        "~",
        "!"
    )
    
    def getFuncFromVar(varName: str):        
        scopes = varName.split("___")
        
        # remove variable name
        scopes.pop(0)
        
        # get list of scope names without scope
        scopelessFuncs = []
        for i in funcMapNames:
            if i.count("___"):
                scopelessFuncs.append(i[: i.index("___")])
            else:
                scopelessFuncs.append(i)
        
        # remove non-function scopes from end of scope
        length = len(scopes)
        for i in range(length):
            if scopes[length - 1 - i] not in scopelessFuncs:
                scopes.pop()
            else:
                break
        
        # remove function name
        funcName = scopes[-1]
        scopes.pop()
        
        # if global return it
        if funcName == "global":
            return funcName
        
        # function name + remaining scopes
        funcName += "___" + "___".join(scopes)
        
        return funcName
    
    def evictReg(name: str, funcName: str):
        
        # funcName is the name of the source function whoes registers contain name
        
        registers = registerStack[owners.index(funcName)]
        LRU = LRUStack[owners.index(funcName)]
        initialisedReg = initialisedRegList[owners.index(funcName)]
        
        varName = registers[int(name[1: ], 0) - 1]
        initialised = initialisedReg[int(name[1: ], 0) - 1]
        
        if varName:
            # get func name for var
            # get correct heap for the found var
            funcName2 = getFuncFromVar(varName)
            heap = heapStack[owners.index(funcName2)]
            
            # get heap return address
            heapIndex = originalHeapLocations[owners.index(currentFuncName)][int(name[1: ], 0) - 1]
            
            # check heap location is correct
            if heap[heapIndex] != varName:
                raise Exception(f"Tried to evict the variable \"{varName}\" into an already occupied heap location")
            
            # write var into heap
            heap[heapIndex] = varName
            
            # mark original register as empty
            registers[int(name[1: ], 0) - 1] = ""
            
            # mark heap return address as empty
            originalHeapLocations[owners.index(currentFuncName)][int(name[1: ], 0) - 1] = ""
            
            # update LRU
            LRU[int(name[1: ], 0) - 1] = max(LRU) + 1
            
            # check initialisation status
            if initialised:
                # STR #heapIndex_funcName2 reg
                URCL.append(["STR", f"#{heapIndex}_{funcName2}", name])
                
                # move initialisation status
                initialisedHeapList[owners.index(funcName2)][heapIndex] = True
                
                # reset reg initialisation status
                initialisedReg[int(name[1: ], 0) - 1] = False
            
        else: # reset LRU but not much else needs to happen here
            
            # update LRU
            LRU[int(name[1: ], 0) - 1] = max(LRU) + 1
        
        return # nothing
    
    def fetchVar(varName: str, invalid: bool = False):
        
        # if number or char return that as an immediate value
        if (varName[0].isnumeric()) or (varName.startswith("'")):
            return varName
        
        # go though all scopes for varName
        while varName.count("___"):
        
            # get func name
            funcName = getFuncFromVar(varName)
            
            # get registers and LRU (target)
            registers = registerStack[owners.index(currentFuncName)]
            LRU = LRUStack[owners.index(currentFuncName)]
            initialisedReg = initialisedRegList[owners.index(currentFuncName)]
            
            # get heap (source)
            heap = heapStack[owners.index(funcName)]
            initialisedHeap = initialisedHeapList[owners.index(funcName)]
            
            if varName in constantVars[owners.index(funcName)]:
                # return value of const (empty string if undefined)
                return constantValues[owners.index(funcName)][constantVars[owners.index(funcName)].index(varName)]
            
            elif varName in registers:
                # update LRU
                for i in range(MINREG):
                    LRU[i] += 1 # increment all other values by 1
                LRU[registers.index(varName)] = 0
                
                # return reg name
                return f"R{registers.index(varName) + 1}" # return the register name that contains the new var (or immediate value)
            
            elif varName in heap:
                # find LRU register
                regIndex = LRU.index(max(LRU))
                
                # evict LRU reg
                evictReg(f"R{regIndex + 1}", currentFuncName)
                
                # get heapIndex of source
                heapIndex = heap.index(varName)
                
                # get return heap location for ALL variables
                # store return heap location
                originalHeapLocations[owners.index(currentFuncName)][regIndex] = heapIndex
                
                # get initialisation status
                initialised = initialisedHeap[heapIndex]
                
                if (not invalid) and initialised:
                    # LOD regName #heapIndex_funcName
                    URCL.append(["LOD", f"R{regIndex + 1}", f"#{heapIndex}_{funcName}"])
                    
                    # set reg initialisation status
                    initialisedReg[regIndex] = True
                
                # update target register
                registers[regIndex] = varName
                
                # do not remove marker from heap
                
                # update target LRU
                for i in range(MINREG):
                    LRU[i] += 1 # increment all other values by 1
                LRU[regIndex] = 0
                
                # return reg name
                return f"R{regIndex + 1}" # return the register name that contains the new var (or immediate value)
            
            elif "[0]" + varName in heap:
                # get heapIndex of source
                heapIndex = heap.index("[0]" + varName)
                
                # return heap location as immediate value (do not update stack or registers or LRU)
                return f"#{heapIndex}_{funcName}"
            
            else:
                # remove outermost scope and try again
                varName = stripScope(varName)
            
        raise Exception(f"Tried to fetch undefined variable: {varName}")
    
    def delete(varName: str):
        
        # get func name
        funcName = getFuncFromVar(varName)
        
        # if the variable is outside of the current scope, crash
        if funcName != currentFuncName:
            raise Exception(f"Deleting varaibles that are outside of the current scope is not supported!\nVariable: {varName}\nFunction that tried to delete it: {currentFuncName}")
        
        # get registers and LRU and original heap owners (current function)
        registers = registerStack[owners.index(currentFuncName)]
        LRU = LRUStack[owners.index(currentFuncName)]
        originalHeap = originalHeapLocations[owners.index(currentFuncName)]
        initialisedReg = initialisedRegList[owners.index(currentFuncName)]
        
        # get heap (source function)
        heap = heapStack[owners.index(funcName)]
        initialisedHeap = initialisedHeapList[owners.index(funcName)]
        
        if varName in constantVars[owners.index(currentFuncName)]:
            # remove constant var from list of constants
            index69 = constantVars[owners.index(currentFuncName)].index(varName)
            constantVars[owners.index(currentFuncName)].pop(index69)
            constantValues[owners.index(currentFuncName)].pop(index69)
        
        elif varName in registers:
            # get regIndex
            regIndex = registers.index(varName)
            
            # remove from registers
            registers[regIndex] = ""
            
            # mark previous location as empty
            originalHeap[regIndex] = ""
            
            # update LRU to empty
            LRU[regIndex] = max(LRU) + 1
            
            # update initialisation status
            initialisedReg[regIndex] = False
            
            # the value must also be removed from the heap
            # get heapIndex
            heapIndex = heap.index(varName)
            
            # remove from heap
            heap[heapIndex] = ""
            
            # update initialisation status
            initialisedHeap[heapIndex] = False
            
        elif varName in heap:
            # get heapIndex
            heapIndex = heap.index(varName)
            
            # remove from heap
            heap[heapIndex] = ""
            
            # update initialisation status
            initialisedHeap[heapIndex] = False
            
        elif "[0]" + varName in heap:
            # get array length
            length = arrayLengths[arrNames.index(varName)]
            
            # remove all indexes in array
            for i in range(length):
                heapIndex = heap.index(f"[{i}]{varName}")
                heap[heapIndex] = ""
                initialisedHeap[heapIndex] = False
            
        else:
            raise Exception(f"Tried to delete undefined variable: {varName}")
            
        return # nothing
    
    def createVar(varName: str, varType: str):
        
        if varName.startswith(tuple(arrNames)):
            raise Exception(f"Tried to define array: {varName} as a variable")
        
        # get func name
        funcName = getFuncFromVar(varName)
        
        # get registers
        registers = registerStack[owners.index(funcName)]
        
        # get LRU
        LRU = LRUStack[owners.index(funcName)]
        
        # get heap
        heap = heapStack[owners.index(funcName)]
        
        # check if var already defined
        if (varName in registers) or (varName in heap) or ("[0]" + varName in heap) or (varName in constantVars):
            raise Exception(f"Tried to define already defined variable: {varName}")
        
        # get reg and heap initialisation lists
        initialisedReg = initialisedRegList[owners.index(funcName)]
        initialisedHeap = initialisedHeapList[owners.index(funcName)]
        
        if varType.startswith("const"):
            # add var to varNames and varTypes
            varNames.append(varName)
            variableTypes.append(varType)
            
            # do not add to heap or registers
            constantVars[owners.index(funcName)].append(varName)
            constantValues[owners.index(funcName)].append("") # starts uninitialised
        
        elif False: # "" in registers:
            # get regIndex
            regIndex = registers.index("")
            
            # update registers
            registers[regIndex] = varName
            
            # update LRU
            for i in range(MINREG):
                LRU[i] += 1
            LRU[regIndex] = 0
            
            # add var to varNames and varTypes
            varNames.append(varName)
            variableTypes.append(varType)
            
            # mark reg as uninitalised
            initialisedReg[regIndex] = False
            
            if "" in heap:
                # get heap index
                heapIndex = heap.index("")
                
                # put into heap
                heap[heapIndex] = varName
                
                # mark reg as uninitalised
                initialisedHeap[heapIndex] = False
                
                # add original owner address
                originalHeapLocations[owners.index(funcName)][regIndex] = heapIndex
            
            else:
                # append to heap
                heap.append(varName)
                
                # get heap index
                heapIndex = len(heap) - 1
                
                # mark reg as uninitalised
                initialisedHeap.append(False)
                
                # add original owner address
                originalHeapLocations[owners.index(funcName)][regIndex] = heapIndex
        
        else:
            # add var to varNames and varTypes
            varNames.append(varName)
            variableTypes.append(varType)
            
            if "" in heap:
                # get heap index
                heapIndex = heap.index("")
                
                # mark reg as uninitalised
                initialisedHeap[heapIndex] = False
                
                # put into heap
                heap[heapIndex] = varName
            
            else:
                # append to heap
                heap.append(varName)
                
                # mark reg as uninitalised
                initialisedHeap.append(False)
        
        return # nothing
    
    def evictRegisters(funcName: str):
        
        # funcName should be the current function scope
        
        # evict each register in turn
        for i in range(MINREG):
            evictReg(f"R{i + 1}", funcName)
        
        return # return nothing
    
    def stripScope(name: str):
        scopes = name.split("___")
        if len(scopes) < 2:
            raise Exception(f"Tried to strip the scope of a token that didn't have one to strip: {name}")
        scopes.pop(-1)
        return "___".join(scopes)
    
    def createArr(name: str):
        
        # scope stripping isn't needed as it is a definition (calls need stripping though)
        # the array type isn't needed as array types cannot change from those found by the preprocess step
        
        # get func name
        funcName = getFuncFromVar(name)
        
        if name not in arrNames:
            raise Exception(f"Array: {name}\nIs not in the list of defined arrays")
        
        # get length
        length = arrayLengths[arrNames.index(name)]
        
        # get heap
        heap = heapStack[owners.index(funcName)]
        initialisedHeap = initialisedHeapList[owners.index(funcName)]
        
        # find if heap contains enough "" in a row to fit the array
        index = 0
        temp = 0
        while index < len(heap):
            if heap[index] == "":
                temp += 1
                if temp == length:
                    break
                index += 1
            else:
                temp = 0
                index += 1
        
        if index < len(heap):
            # insert into heap at index
            for i in range(length):
                heap[index + i] = f"[{i}]{name}"
                initialisedHeap[index + i] = False
            
            # return base index
            return f"#{index}_{currentFuncName}"
            
        else:
            # append to end of heap
            for i in range(length):
                heap.append(f"[{i}]{name}")
                initialisedHeap.append(False)
                
            # return base index
            return f"#{len(heap) - length}_{currentFuncName}"
    
    def getType(name: str):
        # if numeric return "void":
        if name[0].isnumeric():
            return "void"
        
        # if char return "constchar"
        if name.startswith("'"):
            return "constchar"
        
        if name.startswith("[0]"):
            stop = 1
        
        while name.count("___") > 0:
            if name in varNames:
                return variableTypes[varNames.index(name)]
            elif name in funcMapNames:
                return functionTypes[funcMapNames.index(name)]
            elif name in arrNames:
                answer = arrayTypes[arrNames.index(name)]
                if (not answer.endswith("*")) and (answer != "void"):
                    answer += "*"
                return answer
            elif name.startswith("["):
                name2 = name[name.index("]") + 1: ]
                if name2 in arrNames:
                    answer = arrayTypes[arrNames.index(name2)]
                    return answer
                else:
                    name = stripScope(name)
            else:
                name = stripScope(name)
                
        raise Exception(f"Tried to fetch type of undefined token: {name}")
    
    def createTEMP(tempType: str):
        
        nameScope = "___" + "___".join(scope)
        
        num = 0
        while True:
            tempVar = f"__TEMP{num}{nameScope}"
            if (tempVar not in varNames) and (tempVar not in funcMapNames) and (tempVar not in arrNames):
                break
            else:
                num += 1
        
        createVar(tempVar, tempType)
        
        return tempVar # return name of new TEMP
    
    def createListOfLocals():
        
        # get local registers
        registers = registerStack[owners.index(currentFuncName)]
        
        # get local LRU
        LRU = LRUStack[owners.index(currentFuncName)]
        
        # get local heap
        heap = heapStack[owners.index(currentFuncName)]
        
        # create list of all local variables and array values
        localVars = []
        
        # all local vars should have a position in the heap
        for i in heap:
            if i:
                localVars.append(i)
        
        return localVars
    
    def fetchCopyVar(regName: str, varName: str):
        
        # if number or char return that as an immediate value
        if (varName[0].isnumeric()) or (varName.startswith("'")):
            # IMM regName value
            URCL.append(["IMM", regName, varName])
            
            return # nothing
        
        # go though all scopes for varName
        while varName.count("___"):
        
            # get func name
            funcName = getFuncFromVar(varName)
            
            # get registers and LRU (target)
            registers = registerStack[owners.index(currentFuncName)]
            LRU = LRUStack[owners.index(currentFuncName)]
            initialisedReg = initialisedRegList[owners.index(currentFuncName)]
            
            # get heap (source)
            heap = heapStack[owners.index(funcName)]
            initialisedHeap = initialisedHeapList[owners.index(funcName)]
            
            if varName in registers:
                if varName == registers[int(regName[1: ], 0) - 1]:
                    # evict target register
                    evictReg(regName, currentFuncName)
                    
                else:
                    #if varName != registers[int(regName[1: ], 0) - 1]:
                    # evict target register
                    evictReg(regName, currentFuncName)
                    
                    # check register initialisation status
                    if initialisedReg[registers.index(varName)]:
                        if regName != f"R{registers.index(varName) + 1}":
                            # MOV regName oldReg
                            URCL.append(["MOV", regName, f"R{registers.index(varName) + 1}"])
                
                return # nothing
            
            elif varName in heap:
                # evict target register
                evictReg(regName, currentFuncName)
                
                # get heapIndex of source
                heapIndex = heap.index(varName)
                
                # check initialisation status
                if initialisedHeap[heapIndex]:
                    # LOD regName #heapIndex_funcName
                    URCL.append(["LOD", regName, f"#{heapIndex}_{funcName}"])
                
                return # nothing
            
            elif "[0]" + varName in heap:
                # get heapIndex of source
                heapIndex = heap.index("[0]" + varName)
                
                # return heap location as immediate value (do not update stack or registers or LRU)
                return f"#{heapIndex}_{funcName}"
            
            else:
                # remove outermost scope and try again
                varName = stripScope(varName)
            
        raise Exception(f"Tried to fetch copy of undefined variable: {varName}")
    
    def getNextFunctionUp(func: str):
        # split into scope list
        scopes = func.split("___")
        
        # while scopes longer than 1:
        while len(scopes) > 1:
            # remove old func name
            scopes.pop(0)
            
            # move new possible func name from end to start
            end = scopes.pop()
            scopes.insert(0, end)

            # create possible func name
            possibleFunc = "___".join(scopes)
            
            # test if valid func name
            if possibleFunc in funcMapNames:
                # return valid func name
                return possibleFunc
        
        # crash if failed to find func
        raise Exception(f"Failed to find a valid function outside of the current scope (Tip: \"return\" is not valid in the global scope)")
    
    def deleteExactLocals():
        
        # dont use createListOfLocals() as this uses the current func scope instead of exact scope
        fullScope = "___".join(scope)
        
        # get local registers
        registers = registerStack[owners.index(currentFuncName)]
        
        # get local heap
        heap = heapStack[owners.index(currentFuncName)]
        
        # delete only the exact locals (this respects the scope of builtins)
        for var in registers:
            if var.endswith(fullScope):
                delete(var)
        for var in heap:
            if var.endswith(fullScope):
                delete(var)
        
        return # nothing
    
    def getBaseArrayIndex(arrName: str):
        # get func scope of array
        funcName = getFuncFromVar(arrName) # should work for array names too
        
        # get heap
        heap = heapStack[owners.index(funcName)]
        
        """# strip scopes until a valid 
        while arrName.count("___"):
            if "[0]" + arrName in heap:
                break
            else:
                arrName = stripScope(arrName)"""
            
        # get heapIndex of start of array
        heapIndex = heap.index("[0]" + arrName) # arrName should already have the correct scope from preprocess
        
        # return '#' prepended heap address
        return f"#{heapIndex}_{funcName}"
    
    def getInitialisationStatus(varName: str):
        
        # if number or char return True
        if (varName[0].isnumeric()) or (varName.startswith("'")):
            return True
        
        # go though all scopes for varName
        while varName.count("___"):
        
            # get func name
            funcName = getFuncFromVar(varName)
            
            # get registers and LRU
            registers = registerStack[owners.index(currentFuncName)]
            LRU = LRUStack[owners.index(currentFuncName)]
            initialisedReg = initialisedRegList[owners.index(currentFuncName)]
            
            # get heap
            heap = heapStack[owners.index(funcName)]
            initialisedHeap = initialisedHeapList[owners.index(funcName)]
            
            if varName in constantVars[owners.index(funcName)]:
                return bool(constantValues[owners.index(funcName)][constantVars[owners.index(funcName)].index(varName)])
            
            elif varName in registers:
                return initialisedReg[registers.index(varName)]
        
            elif varName in heap:
                # get heapIndex
                heapIndex = heap.index(varName)
                return initialisedHeap[heapIndex]
            
            elif "[0]" + varName in heap:
                # get heapIndex of source
                heapIndex = heap.index("[0]" + varName)
                return initialisedHeap[heapIndex]

            else:
                # remove outermost scope and try again
                varName = stripScope(varName)
        
        raise Exception(f"Tried to fetch initialisation status of undefined variable: {varName}")
    
    def returnEvictRegisters(funcName: str):
        
        # funcName should be the current function scope
        
        # this does a fake evict if the variable is local
        
        # evict each register in turn
        for i in range(MINREG):
            var = registerStack[owners.index(funcName)][i]
            if var:
                func = getFuncFromVar(var)
                length = len(URCL)
                
                evictReg(f"R{i + 1}", funcName)
                
                # get rid of the generated code if var is local
                if (func == funcName) and (length != len(URCL)):
                    URCL.pop()
        
        return # return nothing
    
    URCL = []
    
    registerStack = [["" for i in range(MINREG)] for j in range(len(funcMapNames))]
    LRUStack = [[MINREG for i in range(MINREG)] for j in range(len(funcMapNames))]
    originalHeapLocations = [["" for i in range(MINREG)] for j in range(len(funcMapNames))]
    initialisedRegList = [[False for i in range(MINREG)] for j in range(len(funcMapNames))] # keeps track of which reg vars are initialised
    
    constantVars = [[] for i in range(len(funcMapNames))]
    constantValues = [[] for i in range(len(funcMapNames))]
    
    heapStack = [[] for i in range(len(funcMapNames))]
    initialisedHeapList = [[] for i in range(len(funcMapNames))] # keeps track of which heap vars are initialised
    owners = funcMapNames.copy() # function name of who owns which register/heap/LRU in their respective stacks
    
    scope = ["global"] # contains func names and some builtins (if and while)
    
    ifStatementUniqueNumbers = [] # unique number stack for if statements
    whileStatementUniqueNumbers = []
    uniqueNumber = 0 # this value must be incremented after use
    
    currentFuncName = "global" # name of current func with scope (no builtins!)
    
    arrayBeingDefined = [] # used when defining arrays to keep track of the current name and length
    
    whileHeaderTokens = [] # used to "replay" the while header tokens at the end of a while statement
    
    mainTokenIndex = 0
    while mainTokenIndex < len(code):
        token = code[mainTokenIndex]
        
        # raw number or char
        if (token[0].isnumeric()) or (token.startswith("'")):
            mainTokenIndex += 1
    
        # variable
        elif token.startswith(tuple(varNames)):
            mainTokenIndex += 1
        
        # var type definition
        elif token in varTypes:
            name = code[mainTokenIndex - 1]

            createVar(name, token)
            code.pop(mainTokenIndex)
        
        # function (function call)
        elif token.startswith(tuple(funcMapNames)):
            # get exact function name
            funcCallName = token
            while funcCallName.count("___"):
                if funcCallName in funcMapNames:
                    break
                funcCallName = stripScope(funcCallName)
            
            # find if call is recursive
            recursive = funcCallName in funcMapLocations[funcMapNames.index(funcCallName)]
            
            # find how many inputs that function requires
            numberOfInputs = funcNames[funcMapNames.index(funcCallName)][1]
            
            # get returnType
            returnType = functionTypes[funcMapNames.index(funcCallName)]
            
            # point to the rightmost input var
            mainTokenIndex -= 1
            
            # create list of input vars
            inputVars = code[mainTokenIndex + 1 - numberOfInputs: mainTokenIndex + 1].copy()
            
            if recursive:
                # fetch and push all local variables onto the data stack HPSH
                
                # get list of local variables + array values
                localVars = createListOfLocals()
                
                # fetch each value individually and push onto data stack
                for var in localVars:
                    # do not save temp vars that are inputs to the func
                    if not(var.startswith("__TEMP") and (var in inputVars)):
                        # fetch var
                        regName = fetchVar(var)
                        
                        # only add instructions if the previous instruction isn't popping the same thing (not perfect)
                        if False: # URCL[-1: ]:
                            if URCL[-1] == ["HPOP", regName]:
                                URCL.pop()
                            else:
                                # do not save value if value is const type
                                type1 = getType(var)
                                if not((type1.startswith("const")) or (var.startswith("'")) or (var[0].isnumeric())):
                                    # HPSH regName
                                    URCL.append(["HPSH", regName])
                        else:
                            # do not save value if value is const type
                            type1 = getType(var)
                            if not((var in constantVars[owners.index(getFuncFromVar(var))]) or (var.startswith("'")) or (var[0].isnumeric())):
                                # HPSH regName
                                URCL.append(["HSAV", regName])
            
            # fetch the input vars for the function (right to left, Rx to R1) (HPSH first before registers)
            inputIndex = numberOfInputs - 1
            if inputIndex < MINREG:
                startingRegIndex = inputIndex
            else:
                startingRegIndex = MINREG - 1
            while inputIndex >= 0:
                if inputIndex < MINREG:
                    # setup register to be overwritten (right to left, Rx to R1)
                    LRUStack[owners.index(currentFuncName)][inputIndex] = max(LRUStack[owners.index(currentFuncName)]) + 1
                    
                    # get type of input
                    inputType = getType(code[mainTokenIndex])
                    
                    # get expected input type
                    expectedType = funcNames[funcMapNames.index(funcCallName)][2][inputIndex]
                    
                    # type check
                    if (inputType != expectedType) and (inputType[inputType.find("const") + 5: ] != expectedType) and (inputType != "void") and (expectedType != "void"):
                        raise Exception(f"Input type for function {funcCallName} does not match expected type\nExpected type: {expectedType}\nFound type: {inputType}")
                    
                    # check that var being fetched is initialised
                    if getInitialisationStatus(code[mainTokenIndex]) == False:
                        raise Exception(f"Function call input values cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex]}")
                    
                    # fetch copy of input (right to left)
                    fetchCopyVar(f"R{inputIndex + 1}", code[mainTokenIndex])
                    
                    # if var just fetched is TEMP delete it
                    if code[mainTokenIndex].startswith("__TEMP"):
                        delete(code[mainTokenIndex])
                    
                    # pop input var
                    code.pop(mainTokenIndex)
                    # note that the original func call token has not been popped yet
                    
                else: # HPSH
                    # get type of input
                    inputType = getType(code[mainTokenIndex])
                    
                    # get expected input type
                    expectedType = funcNames[funcMapNames.index(funcCallName)][2][inputIndex]
                    
                    # type check
                    if (inputType != expectedType) and (inputType[inputType.find("const") + 5: ] != expectedType) and (inputType != "void") and (expectedType != "void"):
                        raise Exception(f"Input type for function {funcCallName} does not match expected type\nExpected type: {expectedType}\nFound type: {inputType}")

                    # check that var being fetched is initialised
                    if getInitialisationStatus(code[mainTokenIndex]) == False:
                        raise Exception(f"Function call input values cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex]}")

                    # fetch copy of input (right to left)
                    regName = fetchVar(code[mainTokenIndex])
                    
                    # if var just fetched is TEMP delete it
                    if code[mainTokenIndex].startswith("__TEMP"):
                        delete(code[mainTokenIndex])
                    
                    # HPSH regName
                    URCL.append(["HPSH", regName])
                    
                    # pop input var
                    code.pop(mainTokenIndex)
                mainTokenIndex -= 1 # point to next rightmost input
                inputIndex -= 1
            
            # point to original func call token
            mainTokenIndex += 1
            
            # evict any unused registers with vars in to the heap
            unusedRegisters = MINREG - 1 - startingRegIndex
            for i in range(unusedRegisters):
                regIndex = MINREG - 1 - i
                if registerStack[owners.index(currentFuncName)][regIndex] != "":
                    
                    # find if recursive and var being evicted is being HPSH + HPOP
                    if recursive:
                        varName = registerStack[owners.index(currentFuncName)][regIndex]
                        if varName in localVars:
                            # mark var as invalid as it will be HPOP later
                            initialisedRegList[owners.index(currentFuncName)][regIndex] = False
                    
                    evictReg(f"R{regIndex + 1}", currentFuncName)
            
            # HCAL function
            URCL.append(["HCAL", f".{funcCallName}_FUNCSTART"])
            
            # mark all registers as empty
            for i in range(MINREG):
                LRUStack[owners.index(currentFuncName)][i] = MINREG
                registerStack[owners.index(currentFuncName)][i] = ""
            # assign R1 as the location of a new TEMP var (DO NOT AUTOMATICALLY CREATE THIS VAR - do it manually)
            # mark R1 as the most recently used register (all other registers are still empty)
            tempVar = createTEMP(returnType)
            
            # invalid fetch var - hopefully into R1
            fetchVar(tempVar, True)
            # mark tempVar as initialised
            initialisedRegList[owners.index(currentFuncName)][0] = True
            
            if recursive:
                # fetch each saved local var and overwrite it with HPOP restoring the local vars (using earlier list backwards)
    
                # for every var in localVars backwards
                for var in localVars[: : -1]:
                    # do not restore temp vars that are inputs to the func
                    if not(var.startswith("__TEMP") and (var in inputVars)):
                        # fetch Var (invalid)
                        regName = fetchVar(var, invalid = True)
                    
                        # do not save value if value is const type
                        type1 = getType(var)
                        if not((var in constantVars[owners.index(getFuncFromVar(var))]) or (var.startswith("'")) or (var[0].isnumeric())):
                            # HPOP regName
                            URCL.append(["HRSR", regName])
                    
                            # mark reg as initialised
                            initialisedRegList[owners.index(currentFuncName)][int(regName[1:], 0) - 1] = True
            
            # insert new TEMP into list of tokens
            code[mainTokenIndex] = tempVar
    
        # function type definition
        elif token in funcTypes:
            # get func name
            func = code[mainTokenIndex + 1] # func has the correct scope already
            
            # remove name and type definition
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            
            # evict all registers
            evictRegisters(currentFuncName)
            
            # update currentFuncName
            currentFuncName = func
            
            # update scope
            scope.append(currentFuncName[: currentFuncName.index("___")])
            
            # registers and LRU are already blank
            
            # get the number of inputs
            numberOfInputs = funcNames[funcMapNames.index(currentFuncName)][1]
            
            # JMP to end of function
            URCL.append([f"JMP .{currentFuncName}_FUNCEND"])
            
            # label for start of function (branch location for function calls)
            URCL.append([f".{currentFuncName}_FUNCSTART"])
            
            # get list of inputs
            inputVars = funcNames[funcMapNames.index(currentFuncName)][3] # left to right
            
            # define all input variables
            index = 0
            while index < numberOfInputs:
                if code[mainTokenIndex].startswith(tuple(varNames)):
                    mainTokenIndex += 1
                elif code[mainTokenIndex] in varTypes:
                    # get var name
                    varName = code[mainTokenIndex - 1]
                    
                    if index > (MINREG - 1):
                        # get LRU regIndex
                        regIndex = LRUStack[owners.index(currentFuncName)].index(max(LRUStack[owners.index(currentFuncName)]))
                        
                        # evict the LRU reg
                        evictReg(f"R{regIndex + 1}", currentFuncName)
                        
                        # create variable (it should go into the evicted reg)
                        createVar(varName, code[mainTokenIndex])
                        
                        # HPOP regName
                        URCL.append(["HPOP", f"R{regIndex + 1}"]) # put value into newly created var
                        
                        # mark as initialised
                        initialisedRegList[owners.index(currentFuncName)][regIndex] = True
                        
                    else:
                        # create variable
                        createVar(varName, code[mainTokenIndex]) # defines left to right, R1 to Rx
                        
                        # invalid fetch into registers (hopefully is R1)
                        fetchVar(varName, True)
                        # mark as initialised
                        initialisedRegList[owners.index(currentFuncName)][registerStack[owners.index(currentFuncName)].index(varName)] = True
                    
                    # pop tokens from code
                    code.pop(mainTokenIndex)
                    code.pop(mainTokenIndex - 1)
                    mainTokenIndex -= 1
                    
                    # increment counter
                    index += 1
                else:
                    raise Exception(f"Unexpected token: \"{code[mainTokenIndex]}\" in function definition: {currentFuncName}")
            
            # pop "{" token
            code.pop(mainTokenIndex)
            
        # array
        elif token.startswith(tuple(arrNames)):
            mainTokenIndex += 1
        
        # array type definition
        elif token in arrTypes:
            # get array length
            if not code[mainTokenIndex - 1][0].isnumeric():
                raise Exception("Array length must be a number in array definition!")
            length = int(code[mainTokenIndex - 1], 0)
            
            # get array name
            name = code[mainTokenIndex - 2]
            
            # get base heap location of array
            heapLocation = createArr(name) # "#" prepended string
            
            # remove name, length and arrType tokens
            mainTokenIndex -= 2
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            
            # if next token is "=":
            if code[mainTokenIndex] == "=":
                # define array values
                
                # pop "="
                code.pop(mainTokenIndex)
                
                # pop "arrStart"
                code.pop(mainTokenIndex)
                
                # everything will be defined once the "arrEnd" token is reached naturally
                
                # this will be used by the "arrEnd" so it knows what the array is
                arrayBeingDefined.append((name, length))
                
        # arrEnd
        elif token == "arrEnd":
            # get name and length from arrayBeingDefined stack
            name = arrayBeingDefined[-1][0]
            length = arrayBeingDefined[-1][1]
            arrayBeingDefined.pop()
            
            # get type of elements in the array (for type checks)
            arrayType = arrayTypes[arrNames.index(name)]
            
            # pop "arrEnd"
            code.pop(mainTokenIndex)
            
            # define array values (right to left, [x] to [0])
            for i in range(length):
                # get next token
                mainTokenIndex -= 1
                token = code[mainTokenIndex]
                
                # check that var being fetched is initialised
                if getInitialisationStatus(token) == False:
                    raise Exception(f"Values in an array definition cannot be uninitialised!\nUninitialised variable: {token}")
                
                # fetch var
                regName = fetchVar(token)
                
                # get fetched var type
                targetType = getType(token)
                
                if targetType.startswith("const"):
                    targetType = targetType[5: ]
                # type check
                if (arrayType != targetType) and (targetType != "void") and (arrayType != "void") and (arrayType != f"const{targetType}"):
                    raise Exception(f"Array definition {name} contains an element with the wrong type\nExpected type: {arrayType}\nFound type: {targetType}")
                
                # get target array index and its heap index
                targetIndex = length - 1 - i
                heapIndex = heapStack[owners.index(currentFuncName)].index(f"[{targetIndex}]{name}")
                heapLocation = f"#{heapIndex}_{currentFuncName}"
                
                # STR heapLocation regName
                URCL.append(["STR", heapLocation, regName])
                
                # mark heap location as initialised
                initialisedHeapList[owners.index(currentFuncName)][heapIndex] = True
                
                # remove token
                code.pop(mainTokenIndex)
            
            # fix mainTokenIndex
            #mainTokenIndex -= 1

        # Arr
        elif token == "Arr":
            # a 1 Arr
            
            # get array base index
            arrayLocation = getBaseArrayIndex(code[mainTokenIndex - 2]) # "#" prefixed value
            
            # get array type
            arrayType = getType("[0]" + code[mainTokenIndex - 2])
            
            # check that offset being fetched is initialised
            if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                raise Exception(f"Array index values cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # fetch offset
            regName = fetchVar(code[mainTokenIndex - 1])
            
            # get offset type
            offsetType = getType(code[mainTokenIndex - 1])
            
            # type check if pointer
            if (not offsetType.endswith("*")) and (offsetType != "void"):
                raise Exception(f"Array index is not a pointer type\nExpected type: {arrayType}*\nFound type: {offsetType}")
            
            if arrayType.startswith("const"):
                arrayType2 = arrayType[5: ]
            else:
                arrayType2 = arrayType
            # main type check
            if (arrayType2 != offsetType[: -1]) and (arrayType != "void") and (offsetType != "void"):
                raise Exception(f"Array index type does not match array type\nExpected type: {arrayType2}*\nFound type: {offsetType}")
            
            # delete TEMP offset
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            
            # create TEMP
            tempVar = createTEMP(arrayType2)
            regName2 = fetchVar(tempVar, invalid = True)
            
            # LLOD regName2 arrayLocation regName
            URCL.append(["LLOD", regName2, arrayLocation, regName])
            
            # mark temp as initialised
            initialisedRegList[owners.index(currentFuncName)][int(regName2[1: ], 0) - 1] = True
            
            # pop tokens
            mainTokenIndex -= 2
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            
            # insert TEMP token
            code[mainTokenIndex] = tempVar
            
        # ArrAssign
        elif token == "ArrAssign":
            mainTokenIndex += 1
        
        # UNARY*Assign
        elif token == "UNARY*Assign":
            mainTokenIndex += 1
            
        # break
        elif token == "break":
            # delete exact locals
            deleteExactLocals()
            
            # evict all registers
            evictRegisters(currentFuncName)
            
            # get uniqueNumber (DO NOT pop)
            uniqueNum = whileStatementUniqueNumbers[-1]
            
            # JMP .whileHeader2_END_x
            URCL.append(["JMP", f".whileHeader2_END_{uniqueNum}"])
            
            # pop tokens until "}" found (pay attention to "{" tokens too)
            # get rid of all following tokens until a "}" is found (unreachable code)
            # ignoreCloseSquiggly is initialised based on the number of non-while builtins on scope
            ignoreCloseSquiggly = scope[: : -1].index("while")
            while mainTokenIndex < len(code):
                if code[mainTokenIndex] == "{":
                    ignoreCloseSquiggly += 1
                elif (code[mainTokenIndex] == "}") and (ignoreCloseSquiggly == 0):
                    break
                elif (code[mainTokenIndex] == "}") and (ignoreCloseSquiggly > 0):
                    ignoreCloseSquiggly -= 1
                else:
                    code.pop(mainTokenIndex)
        
        # return
        elif token == "return":
            # get name of next function up (scope-wise)
            funcUp = getNextFunctionUp(currentFuncName)
            
            # get expected return type
            expectedReturnType = functionTypes[funcMapNames.index(currentFuncName)]
            
            # if R1 is a local var and is not the return var, delete it
            varName = registerStack[owners.index(currentFuncName)][0]
            varName2 = code[mainTokenIndex - 1]

            if varName:
                if (varName in heapStack[owners.index(getFuncFromVar(varName))]) and (varName != varName2):
                    delete(varName)
            
            # check that var being fetched is initialised
            if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                raise Exception(f"The variable being returned cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # previous var always should exist
            # fetch copy of previous variable into R1
            fetchCopyVar("R1", code[mainTokenIndex - 1])
            
            # get type of var being returned
            singleType = getType(code[mainTokenIndex - 1])
            
            # type check
            if (singleType != expectedReturnType) and (singleType != "void") and (expectedReturnType != "void"):
                raise Exception(f"Returned type does not match the function return type\nExpected type: {expectedReturnType}\nFound type: {singleType}")
            
            # delete all exact locals
            deleteExactLocals()
            
            # evict all non-local variables from the registers and "evict" all local variables
            returnEvictRegisters(currentFuncName)
            
            # HRET
            URCL.append(["HRET"])
            
            # pop 2 tokens
            mainTokenIndex -= 1
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            
            # get rid of all following tokens until a "}" is found (unreachable code)
            # ignoreCloseSquiggly is initialised based on the number of builitins currently on scope
            func = currentFuncName[: currentFuncName.index("___")]
            ignoreCloseSquiggly = scope[: : -1].index(func)
            while mainTokenIndex < len(code):
                if code[mainTokenIndex] == "{":
                    ignoreCloseSquiggly += 1
                elif (code[mainTokenIndex] == "}") and (ignoreCloseSquiggly == 0):
                    break
                elif (code[mainTokenIndex] == "}") and (ignoreCloseSquiggly > 0):
                    ignoreCloseSquiggly -= 1
                else:
                    code.pop(mainTokenIndex)

        # }
        elif token == "}":
            # find out what scope ended here
            scopeEnd = scope[-1]
            
            # if end of function
            if scopeEnd not in ("if", "while", "elseif", "else"):
                # get old func name
                oldFunc = currentFuncName
                
                # delete all exact locals
                deleteExactLocals()
                
                # evict all registers
                evictRegisters(currentFuncName)
                
                # append return code only if last urcl line wasn't HRET
                if URCL[-1] != ["HRET"]:
                    # set return value to 0
                    URCL.append(["IMM", "R1", "0"])
                    
                    # return
                    URCL.append(["HRET"])
                
                # add label to mark the end of the function definition
                URCL.append([f".{oldFunc}_FUNCEND"])
                
                # pop from scope
                scope.pop()
                
                # get name of outer func
                newFunc = getNextFunctionUp(oldFunc)
                
                # update currentFuncName
                currentFuncName = newFunc
                
                # pop "}"
                code.pop(mainTokenIndex)
                
                # possibly remove any leftover unused tokens here
                
            # elif end of if
            elif scopeEnd == "if":
                # delete exact locals
                deleteExactLocals()
                
                # evict all registers
                evictRegisters(currentFuncName)
                
                # get rid of "if" scope
                scope.pop()
                
                # pop unique number if statement doesn't continue
                # if next token is not "else" or "elseifStart":
                if mainTokenIndex + 1 < len(code):
                    if code[mainTokenIndex + 1] not in ("else", "elseifStart"):
                        # get uniqueNumber (pop)
                        uniqueNum = ifStatementUniqueNumbers.pop()
                    else:
                        # get uniqueNumber (DO NOT pop)
                        uniqueNum = ifStatementUniqueNumbers[-1]
                else:
                    # get uniqueNumber (DO NOT pop)
                    uniqueNum = ifStatementUniqueNumbers[-1]
                
                # JMP to end of else statement (.else_END_x) same number as if
                URCL.append(["JMP", f".else_END_{uniqueNum}"])
                
                # .ifBody_END_x
                URCL.append([f".ifBody_END_{uniqueNum}"])
                
                # pop "}"
                code.pop(mainTokenIndex)
                
                # if statement doesn't continue
                if mainTokenIndex < len(code):
                    if code[mainTokenIndex] not in ("else", "elseifStart"):
                        # .else_END_x
                        URCL.append([f".else_END_{uniqueNum}"])
                else:
                    URCL.append([f".else_END_{uniqueNum}"])
                    
            # elif end of while
            elif scopeEnd == "while":
                # delete exact locals
                deleteExactLocals()
                
                # evict all registers
                evictRegisters(currentFuncName)
                
                # get rid of "while" scope
                scope.pop()
                
                # replace "}" token with "whileHeader2End"
                code[mainTokenIndex] = "whileHeader2End"
                
                # fetch and prepend the saved whileHeader tokens to code
                code = code[: mainTokenIndex] + whileHeaderTokens.pop().copy() + code[mainTokenIndex: ]
                
            # elif end of elseif
            elif scopeEnd == "elseif":
                # delete exact locals
                deleteExactLocals()
                
                # evict all registers
                evictRegisters(currentFuncName)
                
                # get rid of "elseif" scope
                scope.pop()
                
                # get elseif uniqueNumber (pop)
                uniqueNum = ifStatementUniqueNumbers.pop()
                
                # get if uniqueNumber2 (DO NOT pop)
                uniqueNum2 = ifStatementUniqueNumbers[-1]
                
                # JMP to end of else statement (.else_END_x) same number as if
                URCL.append(["JMP", f".else_END_{uniqueNum2}"])
                
                # .elseifBody_END_y
                URCL.append([f".elseifBody_END_{uniqueNum}"])
                
                # pop "}"
                code.pop(mainTokenIndex)
            
                # if statement doesn't continue
                if mainTokenIndex < len(code):
                    if code[mainTokenIndex] not in ("else", "elseifStart"):
                        # .else_END_x
                        uniqueNum = ifStatementUniqueNumbers.pop()
                        URCL.append([f".else_END_{uniqueNum}"])
                else:
                    uniqueNum = ifStatementUniqueNumbers.pop()
                    URCL.append([f".else_END_{uniqueNum}"])
            
            # elif end of else
            elif scopeEnd == "else":
                # delete exact locals
                deleteExactLocals()
                
                # evict all registers
                evictRegisters(currentFuncName)
                
                # get rid of "else" scope
                scope.pop()
                
                # pop "}"
                code.pop(mainTokenIndex)
                
                # pop uniqueNumber (the number left on by the original if)
                uniqueNum = ifStatementUniqueNumbers.pop()
                
                # .else_END_x
                URCL.append([f".else_END_{uniqueNum}"])
                
            else:
                raise Exception(f"Unrecognised scope: {scopeEnd} (issue with compiler not the source SYL code)")
        
        # asm
        elif token == "asm":
            # pop "asm"
            code.pop(mainTokenIndex)
            # pop "{"
            code.pop(mainTokenIndex)
            
            # insert urcl code into output
            urclInstruction = []
            while code[mainTokenIndex] != "}":
                # if end of line
                if code[mainTokenIndex] == ";":
                    URCL.append(urclInstruction.copy())
                    urclInstruction = []
                # elif variable/array name
                elif (code[mainTokenIndex].startswith(tuple(varNames))) or (code[mainTokenIndex].startswith(tuple(arrNames))):
                    # cant check if var is initialised before fetch as idk what the URCL code is going to do with it
                    # fetch var
                    regName = fetchVar(code[mainTokenIndex])
                    # mark as initialised as it might be here
                    initialisedRegList[owners.index(currentFuncName)][int(regName[1: ], 0) - 1] = True
                    urclInstruction.append(regName)
                # else normal URCL token
                else:
                    urclInstruction.append(code[mainTokenIndex])
                    
                # pop the token that was just handled
                code.pop(mainTokenIndex)
            
            # append last asm tokens if they exist
            if urclInstruction:
                URCL.append(urclInstruction.copy())
            
            # pop "}"
            code.pop(mainTokenIndex)
            
        # ;
        elif token == ";":
            
            # maybe remove unused tokens here?
            
            # get rid of ;
            code.pop(mainTokenIndex)
        
        # binary operators
        elif token in binaryOperators:
            # fetch input vars
            rightInput = fetchVar(code[mainTokenIndex - 1])
            rightType = getType(code[mainTokenIndex - 1])
            leftInput = fetchVar(code[mainTokenIndex - 2])
            leftType = getType(code[mainTokenIndex - 2])
            
            # check that vars being fetched are initialised
            if (getInitialisationStatus(code[mainTokenIndex - 1]) == False) and (rightType != "void"):
                raise Exception(f"Binary operator input values cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            if (getInitialisationStatus(code[mainTokenIndex - 2]) == False) and (leftType != "void"):
                raise Exception(f"Binary operator input values cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 2]}")
            
            # type check and get result type
            answer, returnType = binaryOperator(token, "", leftInput, leftType, rightInput, rightType) # 1 or more lines of code for answer
            # answer is currently missing the writeback location

            # delete TEMP values from inputs
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            if code[mainTokenIndex - 2].startswith("__TEMP"):
                delete(code[mainTokenIndex - 2])
            
            # create new TEMP var
            tempVar = createTEMP(returnType)
            tempVarReg = fetchVar(tempVar, invalid=True)
            
            # fix the missing writeback location
            for i in range(len(answer)):
                for j in range(len(answer[i])):
                    if answer[i][j] == "":
                        answer[i][j] = tempVarReg
            
            # add urcl code
            URCL += deepcopy(answer)
            
            # mark temp as initailised
            initialisedRegList[owners.index(currentFuncName)][int(tempVarReg[1: ], 0) - 1] = True
            
            # pop from code
            mainTokenIndex -= 2
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            
            # insert the TEMP var into code
            code[mainTokenIndex] = tempVar
        
        # unary operators
        elif token in unaryOperators:
            # fetch input vars
            singleInput = fetchVar(code[mainTokenIndex - 1])
            singleType = getType(code[mainTokenIndex - 1])
            
            # check that var being fetched is initialised
            if (getInitialisationStatus(code[mainTokenIndex - 1]) == False) and (singleType != "void"):
                raise Exception(f"Unary operator input value cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # if singleInput starts with "#":
            arrayLen = -1
            if singleInput.startswith("#"):
                # fix type
                if not(singleType.endswith("*")) and (singleType != "void"):
                    singleType += "*"
                # get array length
                arrayIndex = arrNames.index(code[mainTokenIndex - 1])
                arrayLen = arrayLengths[arrayIndex]
                
            # type check and get result type
            answer, returnType = unaryOperator(token, "", singleInput, singleType, arrayLen) # 1 or more lines of code for answer
            # answer is currently missing the writeback location
        
            # delete TEMP values from inputs
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
        
            # create new TEMP var
            tempVar = createTEMP(returnType)
            tempVarReg = fetchVar(tempVar, invalid=True)
        
            # fix the writeback register in the answer
            for i in range(len(answer)):
                for j in range(len(answer[i])):
                    if answer[i][j] == "":
                        answer[i][j] = tempVarReg

            # add urcl code
            URCL += deepcopy(answer)
            
            # mark temp as initialised
            initialisedRegList[owners.index(currentFuncName)][int(tempVarReg[1: ], 0) - 1] = True
            
            # pop from code
            mainTokenIndex -= 1
            code.pop(mainTokenIndex)
            
            # insert the TEMP var into code
            code[mainTokenIndex] = tempVar
        
        # assignment operator
        elif token == "=":
            # normal variable assignment
            if ((code[mainTokenIndex - 1].startswith(tuple(varNames))) or (code[mainTokenIndex - 1].startswith(tuple(arrNames))) or (code[mainTokenIndex - 1][0].isnumeric()) or (code[mainTokenIndex - 1].startswith("'"))) and ((code[mainTokenIndex - 2].startswith(tuple(varNames))) or (code[mainTokenIndex - 2].startswith(tuple(arrNames))) or (code[mainTokenIndex - 2][0].isnumeric()) or (code[mainTokenIndex - 2].startswith("'"))):
                # fetch input var
                inputReg = fetchVar(code[mainTokenIndex - 1])
                inputType = getType(code[mainTokenIndex - 1])
                
                # check that var being fetched is initialised
                if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                    raise Exception(f"Assignment operator input value cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
                
                # fetch output var
                outputReg = fetchVar(code[mainTokenIndex - 2])
                expectedType = getType(code[mainTokenIndex - 2])
                
                # const type check
                if (expectedType.startswith("const")) and (not(inputType.startswith("const"))) and (getInitialisationStatus(code[mainTokenIndex - 2])):
                    raise Exception(f"Cannot overwrite constant type variable: {code[mainTokenIndex - 2]}")
                
                # type check
                if (inputType != expectedType) and (inputType[inputType.find("const") + 5: ] != expectedType) and (inputType != "void") and (expectedType != "void"):
                    raise Exception(f"Variable type does not match the type of the value being assigned to it\nExpected type: {expectedType}\nFound type: {inputType}")
                
                # del input var if it is TEMP
                if code[mainTokenIndex - 1].startswith("__TEMP"):
                    delete(code[mainTokenIndex - 1])
                    
                if code[mainTokenIndex - 2] in constantVars[owners.index(getFuncFromVar(code[mainTokenIndex - 2]))]:
                    constantValues[owners.index(getFuncFromVar(code[mainTokenIndex - 2]))][constantVars[owners.index(getFuncFromVar(code[mainTokenIndex - 2]))].index(code[mainTokenIndex - 2])] = inputReg
                    
                    if inputReg.startswith(("R", "#")):
                        raise Exception(f"Cannot assign non-constant value to the constant {code[mainTokenIndex - 2]}")
                    
                else:
                    if outputReg != inputReg:
                        # MOV output input
                        URCL.append(["MOV", outputReg, inputReg])
                    
                    # mark output as initialised
                    initialisedRegList[owners.index(currentFuncName)][int(outputReg[1: ], 0) - 1] = True
                
                # remove tokens
                mainTokenIndex -= 1
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex) # purposely leave the leftside of = value in the code
        
            # ArrAssign (array left side of =)
            elif code[mainTokenIndex - 2] == "ArrAssign":
                # a 0 ArrAssign 5 =
                
                # fetch input var
                inputReg = fetchVar(code[mainTokenIndex - 1])
                inputType = getType(code[mainTokenIndex - 1])
                
                # check that var being fetched is initialised
                if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                    raise Exception(f"Assignment operator input value cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
                
                # get array index
                heapLocation = getBaseArrayIndex(code[mainTokenIndex - 4]) # '#' prepended
                
                # get array type
                expectedType = arrayTypes[arrNames.index(code[mainTokenIndex - 4])]
                
                # const type check
                if expectedType.startswith("const"):
                    raise Exception(f"Cannot overwrite elements in the constant type array: {code[mainTokenIndex - 2]}")
                
                # type check
                if (inputType != expectedType) and (inputType[inputType.find("const") + 5: ] != expectedType) and (inputType != "void") and (expectedType != "void"):
                    raise Exception(f"Variable type does not match the expected type of the array\nExpected type: {expectedType}\nFound type: {inputType}")
                
                # get array offset (AKA the value in the [])
                arrayOffset = fetchVar(code[mainTokenIndex - 3]) # array offset isn't type checked
                
                # check that var being fetched is initialised
                if getInitialisationStatus(code[mainTokenIndex - 3]) == False:
                    raise Exception(f"Array index cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 3]}")
                
                # del input var if it is TEMP
                if code[mainTokenIndex - 1].startswith("__TEMP"):
                    delete(code[mainTokenIndex - 1])
                # del offset var if TEMP
                if code[mainTokenIndex - 3].startswith("__TEMP"):
                    delete(code[mainTokenIndex - 1])
                    
                # LSTR arrayIndex arrayOffset inputReg
                URCL.append(["LSTR", heapLocation, arrayOffset, inputReg])
                
                # mark heap location as initialised
                heapIndex = int(heapLocation[1: heapLocation.index("_")], 0)
                initialisedHeapList[owners.index(currentFuncName)][heapIndex] = True
                
                # pop tokens
                mainTokenIndex -= 4
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
                
            # UNARY*Assign
            elif code[mainTokenIndex - 2] == "UNARY*Assign":
                # p UNARY*Assign 5 =
                
                # fetch input var
                inputReg = fetchVar(code[mainTokenIndex - 1])
                inputType = getType(code[mainTokenIndex - 1])
                
                # fetch variable pointer
                pointerReg = fetchVar(code[mainTokenIndex - 3])
                pointerType = getType(code[mainTokenIndex - 3])
                
                # check that vars being fetched are initialised
                if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                    raise Exception(f"Assignment operator input value cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
                if getInitialisationStatus(code[mainTokenIndex - 3]) == False:
                    raise Exception(f"Cannot dereference an uninitialised pointer!\nUninitialised variable: {code[mainTokenIndex - 3]}")
                
                # type check pointer is pointer
                if (not(pointerType.endswith("*"))) and (pointerType != "void"):
                    raise Exception(f"Pointers must be a pointer type (a type suffixed with '*')\nFound type: {pointerType}")
        
                # get expected type
                expectedType = pointerType[: -1]
                
                # const type check
                if expectedType.startswith("const"):
                    raise Exception(f"Cannot overwrite constant type variable: {code[mainTokenIndex - 2]}")
                
                # type check value being written
                if (inputType != expectedType) and (inputType[inputType.find("const") + 5: ] != expectedType) and (inputType != "void") and (expectedType != "void"):
                    raise Exception(f"Variable type does not match the expected type in assignment\nExpected type: {expectedType}\nFound type: {inputType}")
                
                # STR pointerReg inputReg
                URCL.append(["STR", pointerReg, inputReg]) # the optimiser is going to struggle with this one (unless it knows what M0 is)
                
                # mark heap location as initialised (can't do this as pointer value isn't known) (this will cause issues if writing to an otherwise uninitialised var in the heap)
                
                # delete temp values (both pointer and input)
                if code[mainTokenIndex - 1].startswith("__TEMP"):
                    delete(code[mainTokenIndex - 1])
                if code[mainTokenIndex - 3].startswith("__TEMP"):
                    delete(code[mainTokenIndex - 3])
                
                # pop off tokens
                mainTokenIndex -= 3
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
                code.pop(mainTokenIndex)
            
            else:
                raise Exception(f"Unrecognised assignment: {code[: mainTokenIndex + 1][-5: ]} (issue with compiler not the source SYL code)")
        
        # whileStart
        elif token == "whileStart":
            # make list of all tokens between "whileStart" and "while"
            headerTokens = []
            index = mainTokenIndex
            while index < len(code):
                if code[index] == "while":
                    break
                else:
                    headerTokens.append(code[index])
                    index += 1
            
            # append header tokens to stack
            whileHeaderTokens.append(headerTokens.copy())
            
            # pop "whileStart"
            code.pop(mainTokenIndex)
        
        # while
        elif token == "while":
            # regName = fetch the branch condition variable (must not be pointer type)
            regName = fetchVar(code[mainTokenIndex - 1])
            
            # check that var being fetched is initialised
            if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                raise Exception(f"While condition variable cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # get type
            conditionType = getType(code[mainTokenIndex - 1])
            
            # type check
            if conditionType.endswith("*"):
                raise Exception(f"Invalid type in while statement condition - Type cannot be pointer\nFound type: {conditionType}")
            
            # delete condition var if TEMP
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            
            # create new TEMP var
            tempVar = createTEMP("bool")
            regName2 = fetchVar(tempVar)
            
            if regName2 != regName:
                # MOV regName2 regName
                URCL.append(["MOV", regName2, regName])
            
            # delete new TEMP var
            delete(tempVar)
            
            # evict all registers
            evictRegisters(currentFuncName)
            
            # get new uniqueNumber
            uniqueNum = uniqueNumber
            uniqueNumber += 1
            whileStatementUniqueNumbers.append(uniqueNum)
            
            # conditional branch using regName2 goes to .whileHeader2_END_x if true (BRZ) (end of second while header)
            URCL.append(["BRZ", f".whileHeader2_END_{uniqueNum}", regName2])
            
            # .whileBody_START_x
            URCL.append([f".whileBody_START_{uniqueNum}"])
            
            # get rid of tokens
            mainTokenIndex -= 1
            code.pop(mainTokenIndex) # condition
            code.pop(mainTokenIndex) # "while"
            code.pop(mainTokenIndex) # "{"
            
            # add "while" to scopes
            scope.append("while")
        
        # whileHeader2End
        elif token == "whileHeader2End":
            # 1 whileHeader2End
            
            # regName = fetch the branch condition variable (must not be pointer type)
            regName = fetchVar(code[mainTokenIndex - 1])
            
            # check that var being fetched is initialised
            if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                raise Exception(f"While condition variable cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # get type
            conditionType = getType(code[mainTokenIndex - 1])
            
            # type check
            if conditionType.endswith("*"):
                raise Exception(f"Invalid type in while statement condition - Type cannot be pointer\nFound type: {conditionType}")
            
            # delete condition var if TEMP
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            
            # create new TEMP var
            tempVar = createTEMP("bool")
            regName2 = fetchVar(tempVar)
            
            if regName2 != regName:
                # MOV regName2 regName
                URCL.append(["MOV", regName2, regName])
            
            # delete new TEMP var
            delete(tempVar)
            
            # evict all registers
            evictRegisters(currentFuncName)
            
            # get uniqueNumber (pop)
            uniqueNum = whileStatementUniqueNumbers.pop()
            
            # conditional branch using regName2 goes to whileBody_START_x if true (BNZ) (end of second while header)
            URCL.append(["BNZ", f".whileBody_START_{uniqueNum}", regName2])
            
            # .whileHeader2_END_x
            URCL.append([f".whileHeader2_END_{uniqueNum}"])
            
            # get rid of tokens
            mainTokenIndex -= 1
            code.pop(mainTokenIndex) # condition
            code.pop(mainTokenIndex) # "whileHeader2End"
        
        # if
        elif token == "if":
            # 1 if {
            
            # get branch condition var
            regName = fetchVar(code[mainTokenIndex - 1])
            
            # check that var being fetched is initialised
            if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                raise Exception(f"if condition variable cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # get type
            conditionType = getType(code[mainTokenIndex - 1])
            
            # type check
            if conditionType.endswith("*"):
                raise Exception(f"Invalid type in if statement condition - Type cannot be pointer\nFound type: {conditionType}")
            
            # delete condition var if TEMP
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            
            # create new TEMP var
            tempVar = createTEMP("bool")
            regName2 = fetchVar(tempVar)
            
            if regName2 != regName:
                # MOV regName2 regName
                URCL.append(["MOV", regName2, regName])
            
            # delete new TEMP var
            delete(tempVar)
            
            # evict all registers
            evictRegisters(currentFuncName)
            
            # get new uniqueNumber
            uniqueNum = uniqueNumber
            uniqueNumber += 1
            ifStatementUniqueNumbers.append(uniqueNum)
            
            # conditional branch using regName2 goes to next elseif if true (BRZ) (end of ifBody/start of elseif if it exists)
            URCL.append(["BRZ", f".ifBody_END_{uniqueNum}", regName2])
            
            # get rid of tokens
            mainTokenIndex -= 1
            code.pop(mainTokenIndex) # condition
            code.pop(mainTokenIndex) # "if"
            code.pop(mainTokenIndex) # "{"
            
            # add "if" to scopes
            scope.append("if")
        
        # elseifStart
        elif token == "elseifStart":
            code.pop(mainTokenIndex)
        
        # elseif
        elif token == "elseif":
            # regName = fetch the branch condition variable (must not be pointer type)
            regName = fetchVar(code[mainTokenIndex - 1])
            
            # check that var being fetched is initialised
            if getInitialisationStatus(code[mainTokenIndex - 1]) == False:
                raise Exception(f"elseif condition variable cannot be uninitialised!\nUninitialised variable: {code[mainTokenIndex - 1]}")
            
            # get type
            conditionType = getType(code[mainTokenIndex - 1])
            
            # type check
            if conditionType.endswith("*"):
                raise Exception(f"Invalid type in elseif statement condition - Type cannot be pointer\nFound type: {conditionType}")
            
            # delete condition var if TEMP
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            
            # create new TEMP var
            tempVar = createTEMP("bool")
            regName2 = fetchVar(tempVar)
            
            if regName2 != regName:
                # MOV regName2 regName
                URCL.append(["MOV", regName2, regName])
            
            # delete new TEMP var
            delete(tempVar)
            
            # evict all registers
            evictRegisters(currentFuncName)
            
            # get new uniqueNumber
            uniqueNum = uniqueNumber
            uniqueNumber += 1
            ifStatementUniqueNumbers.append(uniqueNum)
            
            # conditional branch using regName2 goes to next elseif if true (BRZ) (end of ifBody/start of elseif if it exists)
            URCL.append(["BRZ", f".elseifBody_END_{uniqueNum}", regName2])
            
            # get rid of tokens
            mainTokenIndex -= 1
            code.pop(mainTokenIndex) # condition
            code.pop(mainTokenIndex) # "elseif"
            code.pop(mainTokenIndex) # "{"
            
            # add "elseif" to scopes
            scope.append("elseif")
        
        # else
        elif token == "else":
            # add "else" to scopes
            scope.append("else")
            
            # pop tokens
            code.pop(mainTokenIndex) # "else"
            code.pop(mainTokenIndex) # "{"
        
        # in
        elif token == "in":
            # get var
            varName = code[mainTokenIndex - 2]
            regName = fetchVar(varName, invalid=True) # invalid because it is just about to be overwritten
            
            # get port
            port = code[mainTokenIndex - 1]
            
            # don't bother with type checks
            
            # IN regName port
            URCL.append(["IN", regName, port])
            
            # mark reg as initialised
            initialisedRegList[owners.index(currentFuncName)][int(regName[1: ], 0) - 1] = True
            
            # pop tokens
            mainTokenIndex -= 2
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
        
        # out
        elif token == "out":
            # get var
            varName = code[mainTokenIndex - 1]
            regName = fetchVar(varName)
            
            # get port
            port = code[mainTokenIndex - 2]
            
            # don't bother with type checks
            
            if not((regName[0].isnumeric()) or (regName.startswith("'"))):
                # check if initialised
                if (initialisedRegList[owners.index(currentFuncName)][int(regName[1: ], 0) - 1] == False) and (not regName[0].isnumeric()):
                    raise Exception(f"The out function cannot accept unintialised values\nUninitialised variable name: {varName}")
            
            # delete if TEMP
            if code[mainTokenIndex - 1].startswith("__TEMP"):
                delete(code[mainTokenIndex - 1])
            
            # OUT port regName
            URCL.append(["OUT", port, regName])
            
            # pop tokens
            mainTokenIndex -= 2
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
        
        # %port
        elif token.startswith("%"):
            mainTokenIndex += 1
        
        elif token == "del":
            varName = code[mainTokenIndex - 1]
            
            delete(varName)
            
            mainTokenIndex -= 1
            code.pop(mainTokenIndex)
            code.pop(mainTokenIndex)
        
        else:
            raise Exception(f"Unrecognised generate URCL token: {token}")
    
    return URCL, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths










