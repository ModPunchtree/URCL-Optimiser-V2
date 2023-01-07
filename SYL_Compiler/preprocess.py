
from SYL_Compiler.tokeniser import tokenise
from copy import deepcopy

def preprocess(code: list):
    
    types = (
            "int",
            "uint",
            "char",
            "int*",
            "uint*",
            "char*",
            "void",
            "const",
            "bool",
            "bool*"
        )
    
    # simple check for matching braces and for "___"
    openCurly = 0
    closeCurly = 0
    openSquare = 0
    closeSquare = 0
    openSquiggly = 0
    closeSquiggly = 0
    for token in code:
        match token:
            case "(":
                openCurly += 1
            case ")":
                closeCurly += 1
            case "[":
                openSquare += 1
            case "]":
                closeSquare += 1
            case "{":
                openSquiggly += 1
            case "}":
                closeSquiggly += 1
            case _:
                if token.find("___") != -1:
                    raise Exception(f"Tokens in code must not contain \"___\" in: {token}")
    
    if openCurly != closeCurly:
        raise Exception("Mismatched () brackets")
    if openSquare != closeSquare:
        raise Exception("Mismatched [] brackets")
    if openSquiggly != closeSquiggly:
        raise Exception("Mismatched {" + "} brackets")
    
    # convert strings to a list of chars
    index = 0
    while index < len(code):
        token = code[index]
        if token.startswith('"'):
            
            string = []
            for char in token:
                if char != '"':
                    string.append(f"'{char}'")
                    string.append(",")
            if string[-1: ] == [","]:
                string.pop()
            
            if len(string) == 0:
                raise Exception(f"Invalid string: {token}")
            code = code[: index] + string.copy() + code[index + 1: ]
        index += 1
    
    """# fill in missing array definition []
    for index, token in enumerate(code[: -2]):
        if code[index: index + 2] == ["=", "{"]:
            if code[index - 1] != "]":
                code = code[: index] + ["[", "]"] + code[index: ]"""
    
    # fill in missing array defintion lengths
    for index, token in enumerate(code[: -4]):
        if code[index: index + 4] == ["[", "]", "=", "{"]:
            length = 0
            index2 = index + 4
            code[index + 3] = "arrStart"
            if code[index2] != "}":
                length += 1
                index2 += 1
                while code[index2] != "}":
                    if code[index2] == ",":
                        length += 1
                    index2 += 1
                code[index2] = "arrEnd"
            length = str(length)
            code.insert(index + 1, length)
            
    # arrStart and arrEnd
    for index, token in enumerate(code[: -2]):
        if code[index: index + 2] == ["=", "{"]:
            code[index + 1] = "arrStart"
            
            index2 = index + 2
            bad = 0
            while True:
                if (code[index2] == "}") and (bad == 0):
                    break
                elif code[index2] == "}":
                    bad -= 1
                elif code[index2] == "{":
                    bad += 1
                index2 += 1
            
            code[index2] = "arrEnd"
            
    # Combine types
    index = 0
    while index < len(code) - 3:
        token = code[index]
        if token in types:
            if (code[index + 1] == "*") and (code[index + 3] in (";", "=", "(", ",", ")", "[")):
                code.pop(index)
                code.pop(index)
                code.insert(index, token + "*")
        index += 1
    
    # combine const types
    index = 0
    while index < len(code) - 3:
        token = code[index]
        if token == "const":
            if code[index + 1] in types:
                code[index] += code[index + 1]
                code.pop(index + 1)
        index += 1
    
    types = (
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
    
    # combine else if
    index = 0
    while index < len(code) - 3:
        token = code[index]
        if token == "else":
            if code[index + 1] == "if":
                code[index] += code[index + 1]
                code.pop(index + 1)
        index += 1
    
    # combine % and port name
    index = 0
    while index < len(code) - 3:
        if code[index] in (",", "("):
            if code[index + 1] == "%":
                code[index + 1] = code[index + 1] + code[index + 2]
                code.pop(index + 2)
        index += 1
    
    # Create a list of defined variable names
    # Create a list of defined function names
    varNames = []
    variableTypes = []
    funcNames = []
    functionTypes = []
    arrNames = []
    arrayTypes = []
    varNames2 = []
    funcNames2 = []
    arrNames2 = []
    arrayLengths = []
    scope = ["global"]
    newFunc = False
    subArea = ""
    
    def foo(x):
        return x != "___"
    
    asm = False
    for index, token in enumerate(code[: -2]):
        if token in types:
            name = code[index + 1]
            if name == ")":
                pass # typeCast
            elif code[index + 2] in ("=", ";", ",", ")"):
                varNames.append(name + "___" + "___".join(filter(foo, scope)))
                varNames2.append(name)
                variableTypes.append(token)
                code[index + 1] = name + "___" + "___".join(filter(foo, scope))
            elif code[index + 2] == "(":
                inputs = 0
                inputTypes = []
                inputNames = []
                index2 = index + 3
                if index2 < len(code):
                    if code[index2] != ")":
                        inputTypes.append(code[index2])
                        inputs += 1
                        index2 += 1
                        while code[index2] != ")":
                            if code[index2] == ",":
                                inputs += 1
                            elif code[index2] in types:
                                inputTypes.append(code[index2])
                            else:
                                inputNames.append(code[index2] + "___" + "___".join(filter(foo, scope)))
                                if inputNames[-1].endswith("___"):
                                    inputNames[-1] += name
                                else:
                                    inputNames[-1] += "___" + name
                            index2 += 1
                
                newFunc = True
                funcNames.append((name + "___" + "___".join(filter(foo, scope)), inputs, tuple(inputTypes), tuple(inputNames))) # (funcName, numberOfInputs, (input1Type, ...))
                funcNames2.append(name)
                functionTypes.append(token)
                code[index + 1] = name + "___" + "___".join(filter(foo, scope))
                scope.append(name)
                
            elif code[index + 2] == "[":
                arrNames.append(name + "___" + "___".join(filter(foo, scope)))
                arrNames2.append(name)
                if not(code[index + 3][0].isnumeric()):
                    raise Exception(f"Array length must be a number when defining an array")
                arrayLengths.append(int(code[index + 3], 0))
                arrayTypes.append(token)
            
            else:
                raise Exception(f"Unrecognised tokens: {code[index: index + 3]}")
            
        elif token in varNames2:
            code[index] = token + "___" + "___".join(filter(foo, scope))
            
        elif token == "}":
            if asm:
                asm = False
            else:
                scope.pop()
        elif token == "{":
            if code[index - 1] == "asm":
                asm = True
            else:
                if newFunc:
                    newFunc = False
                elif subArea:
                    scope.append(subArea)
                    subArea = ""
                else:
                    scope.append("___")
        elif token in ("if", "elseif", "else", "while"):
            subArea = token
            
    ################################################################
    ################################################################
    
    # combine else if tokens
    index = 0
    while index < len(code) - 1:
        if (code[index] == "else") and (code[index + 1]) == "if":
            code[index] = "elseif"
            code.pop(index + 1)
        index += 1
    
    # create list of funcs names + scope
    funcNamesWithScope = [i[0] for i in funcNames]
    
    # rename non-definition vars, funcs, arrs
    scope = ["global"]
    ignoreOpenSquiggly = 0
    badOpenSquiggly = 0
    for index, token in enumerate(code):
        if token in funcNamesWithScope:
            scope.append(token[: token.index("___")])
            ignoreOpenSquiggly += 1
        elif token in ("if", "while", "elseif", "else"): ######## "elseif" might not exist here
            scope.append(token)
            ignoreOpenSquiggly += 1
        elif token == "{":
            if ignoreOpenSquiggly:
                ignoreOpenSquiggly -= 1
            else:
                badOpenSquiggly += 1
        elif token == "}":
            if badOpenSquiggly:
                badOpenSquiggly -= 1
            else:
                scope.pop()
        elif token in varNames2:
            varName = token + "___" + "___".join(scope)
            # chop off scopes until a match is found
            # the outermost scope is prioritised
            success = False
            while varName.count("___") > 0:
                if varName in varNames:
                    code[index] = varName
                    success = True
                    break
                else:
                    varName = varName[: : -1]
                    varName = varName[varName.index("___") + 3: ]
                    varName = varName[: : -1]
            if not success:
                raise Exception(f"Variable \"{token}\" was never defined")
            # rename variable with correct scope
            code[index] = varName
        elif token in funcNames2:
            funcName = token + "___" + "___".join(scope)
            # chop off scopes until a match is found
            # the outermost scope is prioritised
            success = False
            while funcName.count("___"):
                if funcName in funcNamesWithScope:
                    code[index] = funcName
                    success = True
                    break
                else:
                    funcName = funcName[: : -1]
                    funcName = funcName[funcName.index("___") + 3: ]
                    funcName = funcName[: : -1]
            if not success:
                raise Exception(f"Function \"{token}\" was never defined")
            # rename function with correct scope
            code[index] = funcName
        elif token in arrNames2:
            arrName = token + "___" + "___".join(scope)
            # chop off scopes until a match is found
            # the outermost scope is prioritised
            success = False
            while arrName.count("___") > 0:
                if arrName in arrNames:
                    code[index] = arrName
                    success = True
                    break
                else:
                    arrName = arrName[: : -1]
                    arrName = arrName[arrName.index("___") + 3: ]
                    arrName = arrName[: : -1]
            if not success:
                raise Exception(f"Array \"{token}\" was never defined")
            # rename function with correct scope
            code[index] = arrName
    
    ################################################################
    ################################################################
    
    # old bad code:
    
    """for index, token in enumerate(code):
        if token in varNames2:
            code[index] = varNames[varNames2.index(token)]
        elif token in funcNames2:
            code[index] = funcNames[funcNames2.index(token)][0]
        elif token in arrNames2:
            code[index] = arrNames[arrNames2.index(token)]
    funcNames2 = [i[0] for i in funcNames]"""
    
    ################################################################
    ################################################################
    
    # Make sure there are no names that exist in multiple lists
    for var in varNames:
        if var in funcNames:
            raise Exception(f"Variables and functions cannot have the same name: {var}")
        if var in arrNames:
            raise Exception(f"Variables and arrays cannot have the same name: {var}")
    for func in funcNames:
        if func in arrNames:
            raise Exception(f"Functions and arrays cannot have the same name: {func}")
    
    # Create function call map
    def createFuncMap(code: list, funcNames2: list):
        funcMapNames = ["global"] + [i[0] for i in funcNames]
        funcMapLocations = [[] for i in range(len(funcNames) + 1)]
        scope = ["global"]
        currentFunc = "global"
        newFunc = False
        asm = False
        for index, token in enumerate(code[1: ]):
            if (token in funcNames2) and (code[index] in types):
                scope.append(token)
                currentFunc = token
                newFunc = True
            elif token in funcNames2:
                if token not in funcMapLocations[funcMapNames.index(currentFunc)]:
                    funcMapLocations[funcMapNames.index(currentFunc)].append(token)
            elif token == "asm":
                asm = True
            elif token == "{":
                if newFunc:
                    newFunc = False
                elif asm:
                    pass
                else:
                    scope.append("___")
            elif token == "}":
                if asm:
                    asm = False
                else:
                    scope.pop()
                    # get top func
                    index69 = -1
                    while True:
                        if scope[index69] != "___":
                            currentFunc = scope[index69]
                            break
                        else:
                            index69 -= 1
            else:
                pass
    
        # add funcs that call other funcs to map
        keepGoing = True
        while keepGoing:
            keepGoing = False
            for index in range(len(funcMapLocations)):
                func = funcMapNames[index]
                locations = funcMapLocations[index]
                for index2 in range(len(locations)):
                    location = locations[index2]
                    if location != func:
                        secondaryLocations = funcMapLocations[funcMapNames.index(location)]
                        for l in secondaryLocations:
                            if l not in funcMapLocations[index]:
                                funcMapLocations[index].append(l)
                                keepGoing = True
            
        return funcMapNames, funcMapLocations
    
    funcMapNames, funcMapLocations = createFuncMap(code, [i[0] for i in funcNames])
    
    # Check for any remaining unknown tokens:
    
    operators = (
            "}",
            "{",
            "]",
            "[",
            ")",
            "(",
            "&",
            "*",
            "+",
            "-",
            "~",
            "!",
            "%",
            "/",
            ">>",
            "<<",
            ">=",
            ">",
            "<=",
            "<",
            "!=",
            "==",
            "^",
            "|",
            "&&",
            "||",
            ">>=",
            "<<=",
            "^=",
            "|=",
            "&=",
            "%=",
            "/=",
            "*=",
            "-=",
            "+=",
            "=",
            ",",
            ";"
        )
    
    builtins = (
            "if",
            "else",
            "while",
            "asm",
            "return",
            "break",
            "elseif",
            "arrStart",
            "arrEnd",
            "malloc",
            "fmalloc",
            "free",
            "ffree"
        )
        
    asm = False
    for token in code:
        if token == "asm":
            asm = True
        elif (token == "}") and asm:
            asm = False
        
        if (not asm) and (token not in operators) and (token not in varNames) and (token not in funcNames2) and (token not in arrNames) and (token not in types) and (not (token[: 1].isnumeric())) and (not(token.startswith(("'", '"')))) and (token not in builtins) and (token not in ("in", "out", "sizeof")) and (not(token.startswith("%"))):
            
            if not token.startswith(tuple(varNames + funcNames2 + arrNames)):
                raise Exception(f"Unrecognised or undefined token: {token}")
    
    # detect if code does not call "main" in global scope but defines "main" in global scope
    if "main___global" in funcMapNames:
        if "main___global" not in funcMapLocations[funcMapNames.index("global")]:
            # append call to main if code does not contain its own call to main
            code.append("main___global")
            code.append("(")
            code.append(")")
            code.append(";")
            
    funcMapNames, funcMapLocations = createFuncMap(code, [i[0] for i in funcNames])
    funcNames3 = [i[0] for i in funcNames]
    
    # Remove any function definitions that are never called
    def removeUselessFunc(code: list, funcMapNames: list, funcMapLocations: list, funcNames: list, funcNames2: list):
        i = 0
        while i < len(funcMapNames):
            func = funcMapNames[i]
            if func != "global":
                useless = True
                for index3, locations in enumerate(funcMapLocations):
                    if index3 != i:
                        for location in locations:
                            if func == location:
                                useless = False
                
                if useless:
                    if func in code:
                        index1 = code.index(func) - 1
                        index2 = index1 + 1
                        scope = []
                        while True:
                            if code[index2] == "{":
                                scope.append("___")
                                index2 += 1
                            elif code[index2] == "}":
                                if len(scope) == 1:
                                    break
                                else:
                                    scope.pop()
                                    index2 += 1
                            else:
                                index2 += 1
                        code = code[: index1] + code[index2 + 1: ] # chop out unused func definition
                    funcNames.pop(i - 1)
                    funcNames2.pop(i - 1)
                    functionTypes.pop(i - 1)
                    funcMapNames, funcMapLocations = createFuncMap(code, [i[0] for i in funcNames])
                    i = 0
                else:
                    i += 1
            else:
                i += 1
        return code, funcMapNames, funcMapLocations, funcNames, funcNames2
    
    code, funcMapNames, funcMapLocations, funcNames, funcNames2 = removeUselessFunc(code, funcMapNames, funcMapLocations, funcNames, funcNames2)
    
    funcNames3 = [i[0] for i in funcNames]
    
    # insert 0 into empty return statements
    index = 0
    while index < len(code) - 1:
        if (code[index] == "return") and (code[index + 1] == ";"):
            code.insert(index + 1, "0")
        index += 1
    
    # Aggressive inlining
    keepGoing = True
    while keepGoing:
        keepGoing = False
        index = 0
        while index < len(code) - 1:
            token = code[index + 1]
            if (token in funcNames3) and (code[index] not in types):
                # func call not definition
                locations = funcMapLocations[funcMapNames.index(token)]
                if token not in locations:
                    # not recursive call
                    for index2, token2 in enumerate(code):
                        if token2 == token:
                            good = False
                            if index2 > 0:
                                if code[index2 - 1] in types:
                                    good = True
                            
                            if good:
                                indexStart = index2
                                indexEnd = index2 + 1
                                stack = []
                                while True:
                                    if code[indexEnd] == "{":
                                        stack.append("___")
                                        indexEnd += 1
                                    elif code[indexEnd] == "}":
                                        if len(stack) == 1:
                                            break
                                        else:
                                            stack.pop()
                                            indexEnd += 1
                                    else:
                                        indexEnd += 1

                                inline = code[indexStart: indexEnd][code[indexStart: indexEnd].index("{") + 1: ]
                                
                                numberOfInputs = funcNames[funcNames3.index(token)][1]
                                
                                # get list of callerInputs
                                i = index + 3 # skip (
                                i2 = numberOfInputs
                                callerInputs = []
                                while i2:
                                    i3 = i
                                    temp = []
                                    bracket = 0
                                    while True:
                                        if (code[i3] in (",", ")")) and (bracket == 0):
                                            callerInputs.append(temp.copy())
                                            i2 -= 1
                                            i = i3 + 1
                                            break
                                        
                                        elif code[i3] == ")":
                                            temp.append(code[i3])
                                            bracket -= 1
                                            i3 += 1
                                        elif code[i3] == "(":
                                            temp.append(code[i3])
                                            bracket += 1
                                            i3 += 1
                                        else:
                                            temp.append(code[i3])
                                            i3 += 1
                                
                                # get list of functionInputs
                                functionInputs = funcNames[funcNames3.index(token)][3]
                                functionInputTypes = funcNames[funcNames3.index(token)][2]
                                
                                # find current scope
                                # index + 1 is the index that the scope should be found for
                                goal = index + 1
                                i = 0
                                newFunc = False
                                scope = ["global"]
                                while i != goal:
                                    if i > 0:
                                        if (code[i] in funcNames3) and (code[i - 1] in types):
                                            scope.append(code[i][: code[i].index("___")])
                                            newFunc = True
                                            i += 1
                                        elif code[i] == "{":
                                            if newFunc:
                                                newFunc = False
                                            else:
                                                scope.append("___")
                                            i += 1
                                        elif code[i] == "}":
                                            scope.pop()
                                            i += 1
                                        else:
                                            i += 1
                                    elif code[i] == "{":
                                        if newFunc:
                                            newFunc = False
                                        else:
                                            scope.append("___")
                                        i += 1
                                    elif code[i] == "}":
                                        scope.pop()
                                        i += 1
                                    else:
                                        i += 1
                                inlineScope = "___" + "___".join(filter(foo, scope))
                                
                                # create substitute vars for callerInputs
                                equivalentInput = []
                                for z in range(len(callerInputs)):
                                    var = callerInputs[z]
                                    varType = functionInputTypes[z]
                                    
                                    if (len(var) > 1) or ((not(var[0][0].isnumeric())) and (not(var[0].startswith("'")))):
                                    
                                        # create a new unique var with scope
                                        num = 0
                                        while True:
                                            tempVar = f"__uniqueVar{num}"
                                            if (tempVar not in varNames) and (tempVar not in varNames2):
                                                break
                                            num += 1
                                        tempVar += inlineScope
                                        varNames.append(tempVar)
                                        varNames2.append(tempVar[: tempVar.index("___")])
                                        variableTypes.append(varType)
                                        
                                        # prepend ["type", "var", ";"] to inline
                                        inline = [varType, tempVar, "="] + var + [";"] + inline
                                        
                                        # add new var as a substitute for the func input
                                        equivalentInput.append([tempVar])
                                        
                                    else:
                                        # if var is a single number or char, append directly
                                        equivalentInput.append(var)
                                    
                                # replace input vars in inline
                                i = 0
                                while i < len(inline):
                                    token69 = inline[i]
                                    if token69.startswith(functionInputs):
                                        x = 0 # index
                                        y = 0 # length
                                        for j in range(len(functionInputs)):
                                            if token69.startswith(functionInputs[j]):
                                                if len(functionInputs[j]) > y:
                                                    y = len(functionInputs[j])
                                                    x = j
                                        
                                        inline = inline[: i] + equivalentInput[x] + inline[i + 1: ]
                                        stop = 1
                                        #inline[i] = callerInputs[x]
                                    i += 1
                                
                                # get return type
                                returnType = code[indexStart - 1]
                                
                                # create unique var name
                                num = 0
                                while True:
                                    tempVar = f"__uniqueVar{num}"
                                    if (tempVar not in varNames) and (tempVar not in varNames2):
                                        break
                                    num += 1
                                tempVar += inlineScope
                                varNames.append(tempVar)
                                varNames2.append(tempVar[: tempVar.index("___")])
                                variableTypes.append(returnType)
                                
                                callerInputs = ["".join(i) for i in callerInputs]
                                
                                # create list of all vars created in inline (rename scopes too?)
                                createdVars = []
                                """for var in equivalentInput:
                                    if len(var) == 1:
                                        if not(var[0].startswith("'") or var[0].isnumeric()):
                                            createdVars.append(var[0])"""
                                oldFuncNames = [] # list of old func names
                                newFuncNames = [] # list of new func names
                                oldvarNames = varNames.copy()
                                for i, token69 in enumerate(inline):
                                    #token69 = token69
                                    while token69.count("___"):
                                        
                                        if token69 in callerInputs:
                                            break
                                        elif token69 in varNames:
                                            num = 0
                                            while True:
                                                
                                                
                                                inline[i] = token69[: token69.index("___")] + str(num) + inlineScope
                                                
                                                if token69[: token69.index("___")] + str(num) + inlineScope not in oldvarNames:
                                                    varNames.append(token69[: token69.index("___")] + str(num) + inlineScope)
                                                    varNames2.append(token69[: token69.index("___")] + str(num))
                                                    variableTypes.append(variableTypes[varNames.index(token69)])
                                                    
                                                    if token69 in equivalentInput:
                                                        createdVars.index()
                                                    break
                                                else:
                                                    num += 1
                                            break
                                        elif token69 in funcNames3:
                                            if i != 0:
                                                # check if function definition
                                                if inline[i - 1] in types:
                                                    # get original func stuff
                                                    originalFunc = funcNames[funcNames3.index(token69)]
                                                    originalFunc = list(originalFunc)
                                                    originalFunc[0] = token69[: token69.index("___")] + inlineScope
                                                    originalFunc = tuple(originalFunc)
                                                    
                                                    originalType = functionTypes[funcNames3.index(token69)]
                                                    
                                                    # append to old func list
                                                    oldFuncNames.append(inline[i])
                                                    newFuncNames.append(token69[: token69.index("___")] + inlineScope)
                                                    
                                                    # replace function name
                                                    inline[i] = token69[: token69.index("___")] + inlineScope
                                                    
                                                    # add to list of functions if not in list of functions
                                                    if token69[: token69.index("___")] + inlineScope not in funcNames3:
                                                        funcNames.append(deepcopy(originalFunc))
                                                        funcNames3.append(token69[: token69.index("___")] + inlineScope)
                                                        functionTypes.append(originalType)
                                            break
                                        else:
                                            token69 = token69[: : -1]
                                            token69 = token69[token69.index("___") + 3: ]
                                            token69 = token69[: : -1]
                                    
                                    if i > 0:
                                        if (inline[i] in varNames) and (inline[i - 1] in types):
                                            createdVars.append(inline[i])
                                        elif (inline[i] in varNames) and (inline[i - 1] == "del"):
                                            createdVars.pop(createdVars.index(inline[i]))
                                            stop = 1
                                            stop = 1
                                            stop = 1
                                            stop = 1
                                
                                # replace moved function calls with new function names
                                for i in range(len(inline)):
                                    if inline[i] in oldFuncNames:
                                        inline[i] = newFuncNames[oldFuncNames.index(inline[i])]
                                
                                # replace "return" with ["newVar", "=", "(", returnType, ")", "("] in inline
                                # then insert ")" at end of line
                                i = 0
                                while i < len(inline):
                                    token69 = inline[i]
                                    if token69 == "return":
                                        inline.insert(i, tempVar)
                                        inline[i + 1] = "="
                                        inline.insert(i + 2, "(")
                                        inline.insert(i + 3, returnType)
                                        inline.insert(i + 4, ")")
                                        inline.insert(i + 5, "(")
                                        
                                        i2 = i + 5
                                        EOF = False
                                        while inline[i2] not in (";", "}"):
                                            i2 += 1
                                            if i2 > len(inline):
                                                EOF = True
                                                break
                                            
                                        if EOF:
                                            inline.append(")")
                                        else:
                                            inline.insert(i2 - 1, ")")
                                    i += 1
                                
                                # append ["del", "var", ";"] for all vars in createdVars
                                for var in createdVars:
                                    inline += ["del", var, ";"]
                                    
                                """# append ["del", "var", ";"] for all vars in equivalentInput that are not number/char
                                for var in equivalentInput:
                                    if len(var) == 1:
                                        if not(var[0].startswith("'") or var[0].isnumeric()):
                                            inline += ["del", var[0], ";"]"""
                                
                                # prepend ["returnType", "newVar", ";"] to inline
                                inline = [returnType, tempVar, ";"] + inline
                                
                                # find index of previous ";" or "{" or start of file
                                i = index
                                SOF = False
                                while code[i] not in (";", "{", "}"):
                                    i -= 1
                                    if i < 0:
                                        SOF = True
                                        i = 0
                                        break
                                
                                # find end of func call
                                i3 = index + 1
                                bad = 0
                                while True:
                                    if (code[i3] == ")") and (bad == 1):
                                        break
                                    elif code[i3] == ")":
                                        bad -= 1
                                    elif code[i3] == "(":
                                        bad += 1
                                    i3 += 1
                                
                                # replace original func call with newVar
                                code = code[: index + 1] + [tempVar] + code[i3 + 1: ]
                                
                                # find end of line for func call and del the tempVar
                                code.insert(index + 1 + code[index + 1: ].index(";") + 1, ";")
                                code.insert(index + 1 + code[index + 1: ].index(";") + 1, tempVar)
                                code.insert(index + 1 + code[index + 1: ].index(";") + 1, "del")
                                
                                # insert inline
                                if SOF:
                                    code = inline + code
                                else:
                                    code = code[: i + 1] + inline + code[i + 1: ]
        
                                index = -1
                                
                                funcMapNames, funcMapLocations = createFuncMap(code, [i[0] for i in funcNames])
                                code, funcMapNames, funcMapLocations, funcNames, funcNames3 = removeUselessFunc(code, funcMapNames, funcMapLocations, funcNames, funcNames3)
                                
                                keepGoing = True
                                break
                                
            index += 1
        
        # remove unused varNames
        i = 0
        while i < len(varNames):
            fullVar = varNames[i]
            Var = varNames2[i]
            useful = False
            for token in code:
                if token == fullVar:
                    useful = True
            if not useful:
                varNames.pop(i)
                varNames2.pop(i)
                variableTypes.pop(i)
            else:
                i += 1
    
    # convert non array definitions into UNARY*
    for index, token in enumerate(code[: -1]):
        if code[index + 1] == "[":
            if code[index - 1] not in types:
                tokenList = []
                square = 0
                i = 2
                while True:
                    if (code[index + i] == "]") and (square == 0):
                        break
                    elif code[index + i] == "]":
                        square -= 1
                    elif code[index + i] == "[":
                        square += 1
                    tokenList.append(code[index + i])
                    i += 1
                code = code[: index].copy() + ["*", "("] + [code[index]] + ["+", "("] + tokenList.copy() + [")", ")"] + code[index + i + 1: ]
    
    return code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths










