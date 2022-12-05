
########################################################################################################

## Code Cleaning

########################################################################################################

### Remove Comments:
def removeComments(code: str):
    
    success = False
    
    while code.find("/*") > -1:
        success = True
        code = code[: code.find("/*")] + code[code[: code.find("/*")].find("*/") + 2: ]
    
    code = code.split("\n")
    code = [line + " " for line in code]
    
    for index, line in enumerate(code):
        if line.find("//") != -1:
            success = True
            code[index] = code[index][: line.find("//")]
            
    return code, success

### Unify Spaces
def unifySpaces(code: list):
    
    success = False
    
    for index, line in enumerate(code):
        
        code[index] = code[index].replace("[", " [ ")
        code[index] = code[index].replace("]", " ] ")
        
        while code[index].find("  ") != -1:
            code[index] = code[index].replace("  ", " ")
            success = True
        if code[index].startswith(" "):
            code[index] = code[index][1: ]
            success = True
        
    return code, success

### Remove Empty Lines
def removeEmptyLines(code: list):
    
    success = False
    
    code2 = []
    for line in code:
        if line and (line != [""]) and (line != [" "]):
            code2.append(line)
        else:
            success = True

    return code2, success

### Define Macros
def defineMacros(code: list):
    
    success = False
    
    for index, line in enumerate(code):
        if line.startswith("@DEFINE "):
            raw = line.split(" ")
            tokens = []
            for token in raw:
                if token:
                    tokens.append(token)
            if len(tokens) != 3:
                raise Exception(f"Expected exactly 3 tokens, found {len(tokens)}:\n{line}")
            key = tokens[1]
            definition = tokens[2]
            for index2, line2 in enumerate(code):
                code[index2] = code[index2].replace(key, definition)
            code.pop(index)
            success = True
            
        elif line.startswith("@"):
            raise Exception(f"Unrecognised Macro:\n{line}")
            
    return code, success

### Convert Bases
def convertBases(code: list):
    
    success = False
    
    for index, line in enumerate(code):
        while code[index].find("0b") != -1:
            number = code[code[index].find("0b"): code[code[index].find("0b"): ].find(" ")]
            number = str(int(number, 2))
            code[index] = code[index][: code[index].find("0b")] + number + code[code[code[index].find("0b"): ].find(" "): ]
            
            success = True
        
        while code[index].find("0x") != -1:
            number = code[code[index].find("0x"): code[code[index].find("0x"): ].find(" ")]
            number = str(int(number, 2))
            code[index] = code[index][: code[index].find("0x")] + number + code[code[code[index].find("0x"): ].find(" "): ]
            
            success = True
            
        while code[index].find("0B") != -1:
            number = code[code[index].find("0B"): code[code[index].find("0B"): ].find(" ")]
            number = str(int(number, 2))
            code[index] = code[index][: code[index].find("0B")] + number + code[code[code[index].find("0B"): ].find(" "): ]
            
            success = True
        
        while code[index].find("0X") != -1:
            number = code[code[index].find("0X"): code[code[index].find("0X"): ].find(" ")]
            number = str(int(number, 2))
            code[index] = code[index][: code[index].find("0X")] + number + code[code[code[index].find("0X"): ].find(" "): ]
            
            success = True

        return code, success

### Tokenise
def tokenise(code: list):
    
    code2 = []
    for line in code:
        raw = line.split(" ")
        new = []
        for token in raw:
            if token:
                new.append(token)
        code2.append(new)

    success = True
    
    return code2, success

### Fix BITS Header Syntax (remove headers from code and return the important values)
def fixBITS(code: list):
    
    success = False
    
    MINREG = calculateMINREG(code)
    
    BITS = 16
    for index, line in enumerate(code):
        if line[0] == "BITS":
            BITS = int(line[-1], 0)
            success = True
            code.pop(index)
            break
    
    for index, line in enumerate(code):
        if line[0] == "MINREG":
            success = True
            code.pop(index)
            break
    
    MINHEAP = 0
    for index, line in enumerate(code):
        if line[0] == "MINHEAP":
            MINHEAP = line[-1]
            success = True
            code.pop(index)
            break
    
    MINSTACK = 0
    for index, line in enumerate(code):
        if line[0] == "MINSTACK":
            MINSTACK = line[-1]
            success = True
            code.pop(index)
            break
        
    RUN = "ROM"
    for index, line in enumerate(code):
        if line[0] == "RUN":
            RUN = line[-1]
            success = True
            code.pop(index)
            break
            
    return code, BITS, MINHEAP, MINSTACK, RUN, MINREG, success

### Fix Negative Values
def fixNegativeValues(code: list, BITS: int):
    
    success = False
    
    MAX = 2**BITS
    for index, line in enumerate(code):
        for index2, token in enumerate(line):
            if token.startswith("-"):
                
                number = token[1:]
                if int(number, 0) == 0:
                    number = "0"
                else:
                    number = str(MAX - int(number, 0))
                
                code[index][index2] = number

                success = True

    return code, success

### Convert Defined Immediates
def convertDefinedImmediates(code: list, BITS: int, MINHEAP: str, MINSTACK: str):
    
    success = False
    
    for index, line in enumerate(code):
        if "@BITS" in line:
            code[index][line.index("@BITS")] = str(BITS)
            success = True
            
        if "@MINHEAP" in line:
            code[index][line.index("@MINHEAP")] = MINHEAP
            success = True
        
        if "@MINSTACK" in line:
            code[index][line.index("@MINSTACK")] = MINSTACK
            success = True

        if "@MSB" in line:
            code[index][line.index("@MSB")] = str(2**(BITS - 1))
            success = True
            
        if "@SMSB" in line:
            code[index][line.index("@SMSB")] = str(2**(BITS - 2))
            success = True
        
        if "@MAX" in line:
            code[index][line.index("@MAX")] = str(2**BITS - 1)
            success = True
            
        if "@SMAX" in line:
            code[index][line.index("@SMAX")] = str(2**(BITS - 1) - 1)
            success = True
        
        if "@UHALF" in line:
            floor = BITS // 2
            ceil = floor
            if BITS & 1:
                ceil += 1
            a = ((2**floor) - 1) << ceil
            
            code[index][line.index("@UHALF")] = str(a)
            success = True

        if "@LHALF" in line:
            ceil = BITS // 2
            if BITS & 1:
                ceil += 1
            a = ((2**ceil) - 1)
            
            code[index][line.index("@LHALF")] = str(a)
            success = True

    return code, success

### Relatives to Labels
def relativesToLabels(code: list, uniqueNum: int):
    
    success = False
    
    for index, line in enumerate(code):
        for index2, token in enumerate(line):
            if token.startswith("~+"):
                number = int(token[token.index("~+") + 2: ], 0)

                pointer = index
                while number > 0:
                    if code[pointer][0].startswith("."):
                        pointer += 1
                    else:
                        pointer += 1
                        number -= 1
                
                label = f".___RELATIVE_{uniqueNum}___"
                
                code[index][index2] = label
                code.insert(pointer, [label])
                
                success = True
                
                return relativesToLabels(code, uniqueNum + 1)[: -1] + (success,)
                
            
            elif token.startswith("~-"):
                number = int(token[token.index("~-") + 2: ], 0)

                pointer = index
                while number > 0:
                    if code[pointer][0].startswith("."):
                        pointer -= 1
                    else:
                        pointer -= 1
                        number -= 1
                
                label = f".___RELATIVE_{uniqueNum}___"
                
                code[index][index2] = label
                code.insert(pointer, [label])
                
                success = True
                
                return relativesToLabels(code, uniqueNum + 1)[: -1] + (success,)
            
    return code, uniqueNum, success

### Remove Unused Labels
def removeUnusedLabels(code: list):
    
    success = False
    
    labels = []
    for line in code:
        if line[0].startswith("."):
            labels.append(line[0])

    usefulLabels = []
    for index, line in enumerate(code):
        if len(line) > 1:
            for token in line:
                if token in labels:
                    usefulLabels.append(token)

    for index, line in enumerate(code):
        if line[0].startswith("."):
            if line[0] not in usefulLabels:
                code[index] = [""]
                success = True

    return removeEmptyLines(code)[0], success


### Remove Multi-Labels
def removeMultiLabels(code: list):
    
    success = False
    
    for index, line in enumerate(code):
        if line[0].startswith("."):
            if index + 1 < len(code):
                if code[index + 1][0].startswith("."):
                    label1 = line[0]
                    label2 = code[index + 1][0]
                    
                    for index2, line2 in enumerate(code):
                        for index3, token in enumerate(line2):
                            if token == label2:
                                code[index2][index3] = label1
                    
                    code.pop(index + 1)
                    
                    success = True
                    
                    return removeMultiLabels(code)[0], success
                
    return code, success

### Move DW Values
def moveDWValues(code: list):
    
    success = False
    
    DW = []
    code2 = []
    lastLabels = []
    for line in code:
        if line[0] == "DW":
            DW += lastLabels
            lastLabels = []
            DW.append(line)
        elif line[0].startswith("."):
            lastLabels.append(line)
        else:
            code2 += lastLabels
            lastLabels = []            
            code2.append(line)
    
    code2 += DW
    
    if code2 != code:
        success = True

    return code2, success

### Remove Unreachable Code
def removeUnreachableCode(code: list):
    
    success = False
    
    for index1, line1 in enumerate(code):
        if line1[0] in ("RET", "HLT", "JMP"):
            pointer1 = index1 + 1
            if pointer1 < len(code):
                while pointer1 < len(code):
                    if not code[pointer1][0].startswith("."):
                        code.pop(pointer1)
                        success = True
                        return removeUnreachableCode(code)[0], success
                    else:
                        break
                
    return code, success

### Reduce Registers
def reduceRegisters(code: list):
    
    success = False
    
    usefulRegisters = []
    for line in code:
        for token in line:
            if token.startswith("R"):
                number = int(token[1: ], 0)
                if number not in usefulRegisters:
                    usefulRegisters.append(number)
    
    MINREG = calculateMINREG(code)
    
    pointer = 1
    while pointer <= MINREG:
        if pointer not in usefulRegisters:
            for index, line in enumerate(code):
                for index2, token in enumerate(line):
                    if token == f"R{MINREG}":
                        code[index][index2] = f"R{pointer}"
            usefulRegisters.pop(usefulRegisters.index(MINREG))
            usefulRegisters.append(pointer)
            MINREG = calculateMINREG(code)
            success = True
            
        pointer += 1
    
    return code, MINREG, success

### Recalculate Headers (just MINREG)
def calculateMINREG(code: list):
    
    MINREG = 0
    for line in code:
        for token in line:
            if token.startswith("R"):
                number = int(token[1: ], 0)
                if number > MINREG:
                    MINREG = number

    return MINREG

########################################################################################################

## Main Optimisations

########################################################################################################

def simpleSingleRegisterWriteInstructions():
    return (
        "ADD",
        "RSH",
        "LOD",
        "NOR",
        "SUB",
        "MOV",
        "IMM",
        "LSH",
        "INC",
        "DEC",
        "NEG",
        "AND",
        "OR",
        "NOT",
        "XNOR",
        "XOR",
        "NAND",
        "MLT",
        "DIV",
        "MOD",
        "SRS",
        "BSS",
        "SETE",
        "SETNE",
        "SETG",
        "SETL",
        "SETGE",
        "SETLE",
        "SETC",
        "SETNC",
        "LLOD",
        "SDIV",
        "SSETL",
        "SSETG",
        "SSETLE",
        "SSETGE",
        "ABS"
    )

### Remove R0
def removeR0(code: list):
    
    for index, line in enumerate(code):
        if line[0] in simpleSingleRegisterWriteInstructions():
            if line[1] == "R0":
                code[index] = [""]
    
    code, success = removeEmptyLines(code)
    
    for index, line in enumerate(code):
        for index2, token in enumerate(line):
            if token == "R0":
                code[index][index2] = "0"
                success = True
    
    return code, success

### Remove NOPs
def removeNOPs(code: list):
    
    success = False
    
    for index, line in enumerate(code):
        if line[0] == "NOP":
            code[index] = [""]

    code, success = removeEmptyLines(code)
    
    return code, success

### Immediate Folding
"""def immediateFolding(code: list, BITS: int):

    success = False

    optimisableInstructions = (
        "ADD",
    )
    
    for index, line in enumerate(code):
        """



