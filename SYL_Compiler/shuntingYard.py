
def shuntingYard(code: list, varNames: list, funcNames: list, arrNames: list, funcMapNames: list, funcMapLocations: list, variableTypes: list, functionTypes: list, arrayTypes: list, arrayLengths: list):
    
    def precidence(token: str, funcNames2: list):
        
        braces = (
            "}",
            "{",
            "]",
            "[",
            ")",
            "(",
            "arrEnd",
            "arrStart"
        )
        
        operators = (

            
            "funcPrecidence",
            
            "del",
            
            "int",
            "uint",
            "char",
            "int*",
            "uint*",
            "char*",
            "void",
            "constint",
            "constuint",
            "constchar",
            "constint*",
            "constuint*",
            "constchar*",
            "constvoid",
            
            "intFunc",
            "uintFunc",
            "charFunc",
            "int*Func",
            "uint*Func",
            "char*Func",
            "voidFunc",
            "constintFunc",
            "constuintFunc",
            "constcharFunc",
            "constint*Func",
            "constuint*Func",
            "constchar*Func",
            "constvoidFunc",
            
            "intArr",
            "uintArr",
            "charArr",
            "int*Arr",
            "uint*Arr",
            "char*Arr",
            "voidArr",
            "constintArr",
            "constuintArr",
            "constcharArr",
            "constint*Arr",
            "constuint*Arr",
            "constchar*Arr",
            "constvoidArr",
            
            "ArrAssign",
            "Arr",
            
            "TYPECASTint",
            "TYPECASTuint",
            "TYPECASTchar",
            "TYPECASTint*",
            "TYPECASTuint*",
            "TYPECASTchar*",
            "TYPECASTvoid",
            "TYPECASTconstint",
            "TYPECASTconstuint",
            "TYPECASTconstchar",
            "TYPECASTconstint*",
            "TYPECASTconstuint*",
            "TYPECASTconstchar*",
            "TYPECASTconstvoid",
            
            "sizeof",
            
            "UNARY*",
            "UNARY*Assign",
            "UNARY+",
            "UNARY-",
            "~",
            "!",
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
            "||",
            "=",
            ",",
            "return",
            "break",
            ";"
        )
    
        if token in operators:
            return len(operators) - operators.index(token)
        elif token in funcNames2:
            return len(operators) - operators.index("funcPrecidence")
        elif token in braces:
            return -1
        else:
            raise Exception(f"Unrecognised token in precidence function: {token}")
    
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
    
    operators = (
        
        "del",
        
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
        "constbool*",
        
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
        "constbool*Func",
        
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
        "constbool*Arr",
        
        "ArrAssign",
        "Arr",
        
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
        "UNARY*Assign",
        "UNARY+",
        "UNARY-",
        "~",
        "!",
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
        "||",
        "=",
        ",",
        "return",
        "break",
        ";"
    )
    
    builtins = (
        "if",
        "elseif",
        "else",
        "while"
    )
    
    funcNames2 = [i[0] for i in funcNames]
    
    outputStack = []
    operatorStack = []
    
    isArray = False
    while code:
        token = code.pop(0)
        
        if code[: 2] == ["input10___global", "="]:
            stop = 1
        
        if (token[0].isnumeric()) or (token.startswith(tuple(varNames))) or (token.startswith(tuple(arrNames))) or ((token.startswith(("'", "%"))) and (len(token) > 1)): # number or var or array name or char or %port
            outputStack.append(token)
        
        elif token in operators:
            tokenPrecidence = precidence(token, funcNames2)
            while True:
                if operatorStack:
                    topPrecidence = precidence(operatorStack[-1], funcNames2)
                    if (tokenPrecidence <= topPrecidence) and not((tokenPrecidence == topPrecidence) and (token == "=")):
                        outputStack.append(operatorStack.pop())
                    else:
                        break
                else:
                    break
            if token == ";":
                outputStack.append(token)
            elif token == ",":
                pass
            else:
                operatorStack.append(token)
        elif token in ("{", "arrStart"):
            if isArray:
                raise Exception("You cannot define arrays inside of arrays!")
            if operatorStack:
                if operatorStack[-1] == "=":
                    isArray = True
            while True:
                if operatorStack:
                    if operatorStack[-1] not in ("(", "{", "[", "arrStart"):
                        outputStack.append(operatorStack.pop())
                    else:
                        break
                else:
                    break
            if isArray:
                outputStack.append("arrStart")
                operatorStack.append("arrStart")
            else:
                outputStack.append(token)
                operatorStack.append(token)
        elif token in ("(", "["):
            operatorStack.append(token)
        elif token in (")", "}", "]", "arrEnd"):
            if (token == "}") and isArray:
                token = "arrEnd"
            while True:
                if operatorStack:
                    if operatorStack[-1] != ("(", "{", "[", "arrStart")[(")", "}", "]", "arrEnd").index(token)]:
                        outputStack.append(operatorStack.pop())
                    else:
                        operatorStack.pop()
                        break
                else:
                    break
            if isArray:
                isArray = False
                outputStack.append("arrEnd")
            elif token in ("}", "arrEnd"):
                outputStack.append(token)
            if operatorStack:
                if (operatorStack[-1] in funcNames2) or (operatorStack[-1] in builtins) or (operatorStack[-1] in ("in", "out")):
                    outputStack.append(operatorStack.pop())
        elif (token in funcNames2) or (token in ("in", "out")):
            if operatorStack:
                if operatorStack[-1] in funcTypes:
                    if token in ("in", "out"):
                        raise Exception(f"The builtin \"in\n and \"out\" functions must not have a type prefixed")
                    outputStack.append(operatorStack.pop())
                    outputStack.append(token)
                else:
                    operatorStack.append(token)
            else:
                operatorStack.append(token)
        elif token in builtins:
            if token == "while":
                outputStack.append("whileStart")
            elif token == "elseif":
                outputStack.append("elseifStart")
            operatorStack.append(token)
        elif token == "asm":
            outputStack.append(token)
            depth = -1
            while code:
                if (code[0] == "}") and (depth == 0):
                    outputStack.append(code.pop(0))
                    break
                elif code[0] == "}":
                    depth -= 1
                elif code[0] == "{":
                    depth += 1
                outputStack.append(code.pop(0))

        else:
            raise Exception(f"Unrecognised token in shunting yard: {token}")
        
    outputStack += operatorStack[: : -1]
    
    def foo(x):
        return x != ","
    
    outputStack = list(filter(foo, outputStack))
    
    return outputStack, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths

