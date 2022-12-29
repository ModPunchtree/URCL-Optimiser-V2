

def memoryMap(URCL: list, funcNames: list, funcMapNames: list, funcMapLocations: list, BITS: int, MINREG: int, functionTypes: list):
    
    # create heap map
    heapMap = [0 for i in funcMapNames]
    
    index = 0
    seenFuncs = []
    overallBad = False
    while index < len(funcMapNames):
        func = funcMapNames[index]
        
        # find if conflicting heap locations
        bad = False
        for i in range(index):
            seenLocations = funcMapLocations[i]
            if (func in seenLocations) and (heapMap[index] == heapMap[i]) and (index != i):
                bad = True
                overallBad = True
                
                # add 1 to that funcs mem location
                heapMap[index] += 1
                
                # reset index
                index = 0
        
        for location in funcMapLocations[index]:
            if (heapMap[funcMapNames.index(location)] == heapMap[index]) and (funcMapNames.index(location) != index):
                bad = True
                overallBad = True
                
                # add 1 to that funcs mem location
                heapMap[index] += 1
                
                # reset index
                index = 0
        
        if not bad:
            index += 1
            
        if index == len(funcMapNames) - 1:
            if overallBad:
                overallBad = False
                index = 0
    
    # find out the size of each functions heap
    funcSizes = [0 for i in heapMap]
    
    for func in funcMapNames:
        for line in URCL:
            for token in line:
                if token.startswith("#"):
                    heapLocationName = token[token.index("_") + 1: ]
                    
                    possibleSize = int(token[1: token.index("_")], 0) + 1
                    
                    currentSize = funcSizes[funcMapNames.index(heapLocationName)]
                    
                    if possibleSize > currentSize:
                        funcSizes[funcMapNames.index(heapLocationName)] = possibleSize
    
    # get max size of each individual heap
    heapSizes = [0 for i in range(max(heapMap) + 1)]
    
    for i in range(len(funcSizes)):
        size = funcSizes[i]
        func = funcMapNames[i]
        currentSize = heapSizes[heapMap[i]]
        
        if size > currentSize:
            heapSizes[heapMap[i]] = size
            
    # find and replace # prepended values
    for func in funcMapNames:
        for index1, line in enumerate(URCL):
            for index2, token in enumerate(line):
                if token.startswith("#"):
                    num = int(token[1: token.index("_")], 0)
                    
                    funcName = token[token.index("_") + 1: ]
                    
                    heapName = heapMap[funcMapNames.index(funcName)]
                    
                    baseIndex = 0
                    for i in range(heapName):
                        baseIndex += heapSizes[i]
                        
                    num += baseIndex
                    
                    URCL[index1][index2] = f"M{num}"
    
    
    URCL.insert(0, ["MINSTACK", "0", "// does not use software stack"])
    
    # generate MINHEAP header
    value = sum(heapSizes)
    URCL.insert(0, ["MINHEAP", str(value)])
    
    URCL.insert(0, ["MINREG", str(MINREG)])
    URCL.insert(0, ["BITS", str(BITS)])
    
    return URCL


