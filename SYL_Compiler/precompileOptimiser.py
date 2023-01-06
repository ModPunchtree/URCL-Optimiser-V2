
def precompileOptimiser(code: list, varNames: list, funcNames: list, arrNames: list, funcMapNames: list, funcMapLocations: list, BITS: int, MINREG: int, variableTypes: list, functionTypes: list, arrayTypes: list, arrayLengths: list):

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
    
    MAX = (2**BITS) - 1
    
    def stripScope(name: str):
        scopes = name.split("___")
        if len(scopes) < 2:
            raise Exception(f"Tried to strip the scope of a token that didn't have one to strip: {name}")
        scopes.pop(-1)
        return "___".join(scopes)
    
    # constant folding
    def constantFold(code: list):
        
        success = False
        
        index = 0
        while index < len(code):
            if code[index] in binaryOperators:
                if code[index - 1][0].isnumeric() and code[index - 2][0].isnumeric():
                    match code[index]:
                        case "%":
                            answer = [str(int(code[index - 2], 0) % int(code[index - 1], 0))]
                        case "/":
                            answer = [str(int(code[index - 2], 0) // int(code[index - 1], 0))]
                        case "BINARY*":
                            answer = [str((int(code[index - 2], 0) * int(code[index - 1], 0)) & MAX)]
                        case "BINARY-":
                            answer = [str((int(code[index - 2], 0) + (MAX - int(code[index - 1], 0)) + 1) & MAX)]
                        case "BINARY+":
                            answer = [str((int(code[index - 2], 0) + int(code[index - 1], 0)) & MAX)]
                        case ">>":
                            answer = [str(int(code[index - 2], 0) >> int(code[index - 1], 0))]
                        case "<<":
                            answer = [str((int(code[index - 2], 0) << int(code[index - 1], 0)) & MAX)]
                        case ">=":
                            if int(code[index - 2], 0) >= int(code[index - 1], 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case ">":
                            if int(code[index - 2], 0) > int(code[index - 1], 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case "<=":
                            if int(code[index - 2], 0) <= int(code[index - 1], 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case "<":
                            if int(code[index - 2], 0) < int(code[index - 1], 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case "!=":
                            if int(code[index - 2], 0) != int(code[index - 1], 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case "==":
                            if int(code[index - 2], 0) == int(code[index - 1], 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case "BINARY&":
                            answer = [str(int(code[index - 2], 0) & int(code[index - 1], 0))]
                        case "^":
                            answer = [str(int(code[index - 2], 0) ^ int(code[index - 1], 0))]
                        case "|":
                            answer = [str(int(code[index - 2], 0) | int(code[index - 1], 0))]
                        case "&&":
                            if (int(code[index - 2], 0) > 0) and (int(code[index - 1], 0) > 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case "||":
                            if (int(code[index - 2], 0) > 0) or (int(code[index - 1], 0) > 0):
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case _:
                            raise Exception("Unknown token in PCO")
                        
                    if answer != code[index - 2: index + 1]:
                        success = True
                    code = code[: index - 2] + answer + code[index + 1: ]
                    index -= 2
                else:
                    index += 1
                
            elif code[index] in unaryOperators:
                if code[index - 1][0].isnumeric():
                    match code[index]:
                        case "TYPECASTint":
                            answer = [code[index - 1]]
                        case "TYPECASTuint":
                            answer = [code[index - 1]]
                        case "TYPECASTchar":
                            answer = [code[index - 1]]
                        case "TYPECASTint*":
                            answer = [code[index - 1]]
                        case "TYPECASTuint*":
                            answer = [code[index - 1]]
                        case "TYPECASTchar*":
                            answer = [code[index - 1]]
                        case "TYPECASTvoid":
                            answer = [code[index - 1]]
                        case "TYPECASTbool":
                            answer = [code[index - 1]]
                        case "TYPECASTbool*":
                            answer = [code[index - 1]]
                        case "TYPECASTconstint":
                            answer = [code[index - 1]]
                        case "TYPECASTconstuint":
                            answer = [code[index - 1]]
                        case "TYPECASTconstchar":
                            answer = [code[index - 1]]
                        case "TYPECASTconstint*":
                            answer = [code[index - 1]]
                        case "TYPECASTconstuint*":
                            answer = [code[index - 1]]
                        case "TYPECASTconstchar*":
                            answer = [code[index - 1]]
                        case "TYPECASTconstvoid":
                            answer = [code[index - 1]]
                        case "TYPECASTconstbool":
                            answer = [code[index - 1]]
                        case "TYPECASTconstbool*":
                            answer = [code[index - 1]]
                        case "sizeof":
                            answer = ["1"]
                        case "UNARY*":
                            answer = [code[index - 1], code[index]]
                        case "UNARY+":
                            answer = [code[index - 1]]
                        case "UNARY-":
                            answer = [str((MAX - int(code[index - 1], 0) + 1) & MAX)]
                        case "~":
                            answer = [str(MAX - int(code[index - 1], 0))]
                        case "!":
                            if int(code[index - 1], 0) > 0:
                                answer = [str(MAX)]
                            else:
                                answer = ["0"]
                        case _:
                            raise Exception("Unknown token in PCO")

                    if answer != code[index - 2: index + 1]:
                        success = True
                    code = code[: index - 1] + answer + code[index + 1: ]
                    index -= 1
                else:
                    index += 1

            else:
                index += 1
                
        return code, success

    # sizeof(x)
    def sizeofFolding(code: list):
        
        success = False
        
        index = 0
        while index < len(code):
            if code[index] == "sizeof":
                name = code[index - 1]
                while True:
                    if name in varNames:
                        answer = ["1"]
                        break
                    elif name in funcMapNames:
                        answer = ["1"]
                        break
                    elif name in arrNames:
                        answer = [str(arrayLengths[arrNames.index(name)])]
                        break
                    elif name.startswith("["):
                        answer = ["1"]
                        break
                    else:
                        if name.count("___"):
                            name = stripScope(name)
                        else:
                            raise Exception(f"Unknown sizeof token: {code[index - 1]}")
                
                code = code[: index - 1] + answer + code[index + 1: ]
                success = True
                index -= 1
            
            else:
                index += 1
        
        return code, success
    
    ###########################################################
    
    # main
    overallSuccess = True
    while overallSuccess:
        
        overallSuccess = False
        
        # constant folding
        code, success = constantFold(code)
        overallSuccess |= success
        
        # sizeof
        code, success = sizeofFolding(code)
        overallSuccess |= success

    return code






