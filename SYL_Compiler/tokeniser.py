
def tokenise(rawCode: str):
    
    symbols = (
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
        ">",
        "<",
        "=",
        "^",
        "|",
        ",",
        ";"
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
    
    def fetchString(index: int, rawCode: str):
        answer = ""
        while index < len(rawCode):
            char = rawCode[index]
            if char.isalpha() or char.isnumeric() or char == "_":
                answer += char
                index += 1
            else:
                return answer, index
            
    def fetchNumber(index: int, rawCode: str):
        base = 0
        answer = ""
        while index + base < len(rawCode):
            char = rawCode[index + base]
            if char.isnumeric():
                answer += char
                base += 1
            elif (base == 1) and (char in ("x", "X", "b", "B")):
                answer += char
                base += 1
            else:
                return str(int(answer, 0)), index + base
    
    def fetchSymbol(index: int, rawCode: str):
        
        triple = rawCode[index: index + 3]
        if triple in operators:
            return triple, index + 3
        
        double = rawCode[index: index + 2]
        if double in operators:
            return double, index + 2
        
        single = rawCode[index: index + 1]
        if single in operators:
            return single, index + 1
        
        raise Exception(f"Unrecognised symbol: {single}")
    
    def fetchSingleQuote(index: int, rawCode: str):
        answer = "'"
        index += 1
        while index < len(rawCode):
            char = rawCode[index]
            if char != "'":
                answer += char
                index += 1
            else:
                return answer + "'", index + 1
    
    def fetchDoubleQuote(index: int, rawCode: str):
        answer = '"'
        index += 1
        while index < len(rawCode):
            char = rawCode[index]
            if char != '"':
                answer += char
                index += 1
            else:
                return answer + '"', index + 1
    
    # remove multiline comments
    while rawCode.count("/*") != 0:
        rawCode = rawCode[: rawCode.index("/*")] + rawCode[rawCode.index("/*"): ][rawCode[rawCode.index("/*"): ].index("*/") + 2: ]
    
    # remove line comments
    while rawCode.count("//") != 0:
        rawCode = rawCode[: rawCode.index("//")] + rawCode[rawCode.index("//"): ][rawCode[rawCode.index("//"): ].index("\n") + 1: ]
    
    # tokenise
    code = []
    index = 0
    while index < len(rawCode):
        char = rawCode[index]
        if char.isalpha() or char == "_":
            token, index = fetchString(index, rawCode)
            code.append(token)
            
            if token == "asm":
                char = rawCode[index]
                t = ""
                asm = []
                while char != "}":
                    if char not in (" ", ";", "\n"):
                        t += char
                    elif char == ";":
                        if t:
                            asm.append(t)
                            t = ""
                        asm.append(char)
                    else:
                        if t:
                            asm.append(t)
                            t = ""
                    index += 1
                    char = rawCode[index]
                    
                code += asm
            
        elif char.isnumeric():
            token, index = fetchNumber(index, rawCode)
            code.append(token)
        elif char == " ":
            index += 1
        elif char == "\n":
            if code:
                if (code[-1]) and (code[-1] not in (";", "{", "}")):
                    raise Exception("Code is missing a ;")
            index += 1
        elif char in symbols:
            token, index = fetchSymbol(index, rawCode)
            code.append(token)
        elif char == "'":
            token, index = fetchSingleQuote(index, rawCode)
            code.append(token)
        elif char == '"':
            token, index = fetchDoubleQuote(index, rawCode)
            code.append(token)
        else:
            raise Exception(f"Unrecognised char: {char}")
    
    return code