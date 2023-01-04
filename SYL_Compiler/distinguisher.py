
def distinguisher(code: list, varNames: list, funcNames: list, arrNames: list, funcMapNames: list, funcMapLocations: list, variableTypes: list, functionTypes: list, arrayTypes: list, arrayLengths: list):
    
    polariseable = (
        "+",
        "-",
        "&",
        "*"
    )
    
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
    
    # operator polarity
    code.insert(0, "")
    for index, token in enumerate(code):
        if token in polariseable:
            if (code[index - 1] not in operators) or (code[index - 1] == ")"):
                code[index] = f"BINARY{token}"
            else:
                code[index] = f"UNARY{token}"
                if code[index] == "UNARY&":
                    raise Exception(f"UNARY& is not supported")
    code.pop(0)
    
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
    
    typeCasts = (
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
        "TYPECASTconstbool*"
    )
    
    funcNames2 = [i[0] for i in funcNames]
    # type definitions and typecasts
    for index, token in enumerate(code):
        if token in types:
            if code[index + 1] in varNames:
                pass
            elif code[index + 1] in funcNames2:
                code[index] = funcTypes[types.index(token)]
            elif code[index + 1] in arrNames:
                code[index] = arrTypes[types.index(token)]
            elif code[index + 1] == ")":
                if code[index - 1] == "(":
                    code[index + 1] = ""
                    code[index - 1] = ""
                    code[index] = typeCasts[types.index(token)]

    def foo(x):
        return bool(x)
    
    code = list(filter(foo, code))
    
    badAssignments = (
        "+=",
        "-=",
        "*=",
        "/=",
        "%=",
        "&=",
        "|=",
        "^=",
        "<<=",
        ">>="
    )
    
    # convert += -= *= /= %= &= |= ^= <<= >>= into =
    index = 0
    while index < len(code):
        token = code[index]
        if token in badAssignments:
            SOF = False
            indexStartOfLine = index
            while indexStartOfLine > 0:
                if code[indexStartOfLine] in (";", "}", "{", "="):
                    break
                indexStartOfLine -= 1
                if indexStartOfLine < 0:
                    indexStartOfLine = 0
                    SOF = True
                    break
            if SOF:
                code = code[: index] + ["="] + code[: index] + [token[: -1]] + code[index + 1: ]
            else:
                code = code[: index] + ["="] + code[indexStartOfLine + 1: index] + [token[: -1]] + code[index + 1:]
            index = -1
        index += 1
    
    # operator polarity (again lol)
    code.insert(0, "")
    for index, token in enumerate(code):
        if token in polariseable:
            if code[index - 1] not in operators:
                code[index] = f"BINARY{token}"
            else:
                code[index] = f"UNARY{token}"
                raise Exception(f"UNARY& is not supported")
    code.pop(0)
    
    # find references to arrays (not definitions)
    # distinguish left and right of the = sign
    index = 0
    while index < len(code):
        token = code[index]
        if token in arrNames:
            if code[index - 1] not in arrTypes:
                if code[index + 1] == "[":
                    # detect if array is on the left side of a "="
                    indexEquals = index
                    indexRightSquare = index
                    leftOfEquals = False
                    squareStack = -1
                    while indexEquals < len(code):
                        if (code[indexEquals] == "]") and (squareStack == 0):
                            if indexEquals + 1 < len(code):
                                if code[indexEquals + 1] == "=":
                                    leftOfEquals = True
                                    indexRightSquare = indexEquals
                                    indexEquals += 1
                                    break
                                else:
                                    indexRightSquare = indexEquals
                                    break
                            else:
                                indexRightSquare = indexEquals
                                break
                        elif code[indexEquals] == "]":
                            squareStack -= 1
                            indexEquals += 1
                            indexRightSquare += 1
                        elif code[indexEquals] == "[":
                            squareStack += 1
                            indexEquals += 1
                            indexRightSquare += 1
                        else:
                            indexEquals += 1
                            indexRightSquare += 1
                    
                    if leftOfEquals:
                        code.insert(indexEquals, "ArrAssign")
                    else:
                        code.insert(indexRightSquare + 1, "Arr")
                    
        index += 1
    
    # find UNARY* - if left of "=" then turn it into UNARY*Assign
    for index, token in enumerate(code):
        if token == "UNARY*":
            index2 = index
            while index2 < len(code):
                if code[index2] == "=":
                    code[index] = "UNARY*Assign"
                    break
                elif code[index2] in (";", "}", "{"):
                    break
                index2 += 1
    
    return code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths

