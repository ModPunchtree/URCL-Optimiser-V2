
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

### Shortcut Branches
def shortcutBranches(code: list):
    
    branches = (
        "BGE",
        "JMP",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BOD",
        "BEV",
        "BLE",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "CAL",
        "BRC",
        "BNC",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE"
    )
    
    success = False
    
    for index, line in enumerate(code):
        if line[0] in branches:
            location1 = line[1]
            if location1.startswith("."):
                line2 = code[code.index([location1]) + 1]
                if line2[0] == "JMP":
                    location2 = line2[1]
                    code[index][1] = location2
                    success = True
    
    return code, success

### Remove Pointless Branches
def pointlessBranches(code: list):
    
    simpleBranches = (
        "BGE",
        "JMP",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BOD",
        "BEV",
        "BLE",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "BRC",
        "BNC",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE"
    )
    
    for index, line in enumerate(code):
        if line[0] in simpleBranches:
            location = line[1]
            if index + 1 < len(code):
                if code[index + 1] == [location]:
                    code[index] = [""]
    
    code, success = removeEmptyLines(code)
    
    return code, success

### JMP to Subroutine
def JMP2Subroutine(code: list):
    
    success = False
    
    simpleBranches = (
        "BGE",
        "JMP",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BOD",
        "BEV",
        "BLE",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "BRC",
        "BNC",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE"
    )
    
    for index, line in enumerate(code):
        if line[0] == "JMP":
            location1 = line[1]
            if location1.startswith("."):
                line2 = code[code.index([location1]) + 1]
                if line2[0] == "CAL":
                    code[index] = code[code.index([location1])].copy()
                    success = True
                elif line2[0] == "RET":
                    code[index] = code[code.index([location1])].copy()
                    success = True
    
        elif line[0] == "CAL":
            location1 = line[1]
            if location1.startswith("."):
                line2 = code[code.index([location1]) + 1]
                if line2[0] == "RET":
                    code[index] = [""]
                elif line2[0] == "JMP":
                    location2 = line2[1]
                    code[index][1] = location2
                    success = True
                elif line2[0] == "HLT":
                    code[index] = ["HLT"]
                    success = True
    
    code, success2 = removeEmptyLines(code)
    success |= success2
    
    return code, success

### Immediate Folding (100% solvable instructions)
def fullImmediateFolding(code: list, BITS: int):
    
    success = False

    optimisableInstructions = (
        "ADD",
        "RSH",
        "BGE",
        "NOR",
        "SUB",
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
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BOD",
        "BEV",
        "BLE",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "BRC",
        "BNC",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
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
        "SDIV",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE",
        "SSETL",
        "SSETG",
        "SSETLE",
        "SSETGE",
        "ABS"
    )
    
    imm2and3 = (
        "ADD",
        "BGE",
        "NOR",
        "SUB",
        "AND",
        "OR",
        "XNOR",
        "XOR",
        "NAND",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BLE",
        "BRC",
        "BNC",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
        "BSS",
        "SETE",
        "SETNE",
        "SETG",
        "SETL",
        "SETGE",
        "SETLE",
        "SETC",
        "SETNC",
        "SDIV",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE",
        "SSETL",
        "SSETG",
        "SSETLE",
        "SSETGE"
    )
    
    imm2Only = (
        "RSH",
        "LSH",
        "INC",
        "DEC",
        "NEG",
        "NOT",
        "BOD",
        "BEV",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "SRS",
        "ABS"
    )
    
    MAX = 2**BITS - 1
    MSB = 2**(BITS - 1)
    
    for index, line in enumerate(code):
        if line[0] in imm2and3:
            if (line[2][0: ].isnumeric()) and (line[3][0: ].isnumeric()):
                imm2 = int(line[2], 0)
                imm3 = int(line[3], 0)
                
                answer = [f"Unrecognised Instruction: {line[0]}"]
                match line[0]:
                    case "ADD":
                        number = (imm2 + imm3) & MAX
                        answer = ["IMM", line[1], str(number)]
                        
                    case "BGE":
                        if imm2 >= imm3:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                        
                    case "NOR":
                        number = MAX - (imm2 | imm3)
                        answer = ["IMM", line[1], str(number)]
                    
                    case "SUB":
                        number = (imm2 + (MAX - imm3) + 1) & MAX
                        answer = ["IMM", line[1], str(number)]
                    
                    case "AND":
                        number = imm2 & imm3
                        answer = ["IMM", line[1], str(number)]
                    
                    case "OR":
                        number = imm2 | imm3
                        answer = ["IMM", line[1], str(number)]
                    
                    case "XNOR":
                        number = MAX - (imm2 ^ imm3)
                        answer = ["IMM", line[1], str(number)]

                    case "XOR":
                        number = imm2 ^ imm3
                        answer = ["IMM", line[1], str(number)]

                    case "NAND":
                        number = MAX - (imm2 & imm3)
                        answer = ["IMM", line[1], str(number)]

                    case "BRL":
                        if imm2 < imm3:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "BRG":
                        if imm2 > imm3:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "BRE":
                        if imm2 == imm3:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                            
                    case "BNE":
                        if imm2 != imm3:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "BLE":
                        if imm2 <= imm3:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                        
                    case "BRC":
                        if (imm2 + imm3) > MAX:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "BNC":
                        if (imm2 + imm3) <= MAX:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]

                    case "MLT":
                        number = (imm2 * imm3) & MAX
                        answer = ["IMM", line[1], str(number)]

                    case "DIV":
                        number = imm2 // imm3
                        answer = ["IMM", line[1], str(number)]

                    case "MOD":
                        number = imm2 % imm3
                        answer = ["IMM", line[1], str(number)]

                    case "BSR":
                        number = imm2 >> imm3
                        answer = ["IMM", line[1], str(number)]

                    case "BSL":
                        number = (imm2 << imm3) & MAX
                        answer = ["IMM", line[1], str(number)]

                    case "BSS":
                        sign = imm2 & MSB
                        if sign:
                            number = MAX - ((MAX - imm2) >> imm3)
                        else:
                            number = imm2 >> imm3
                        answer = ["IMM", line[1], str(number)]
                    
                    case "SETE":
                        if imm2 == imm3:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                        
                    case "SETNE":
                        if imm2 != imm3:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                    
                    case "SETG":
                        if imm2 > imm3:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                            
                    case "SETL":
                        if imm2 < imm3:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                            
                    case "SETGE":
                        if imm2 >= imm3:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                            
                    case "SETLE":
                        if imm2 <= imm3:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]

                    case "SETC":
                        if (imm2 + imm3) > MAX:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]

                    case "SETNC":
                        if (imm2 + imm3) <= MAX:
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]

                    case "SDIV":
                        sign2 = imm2 & MSB
                        if sign2:
                            imm2 = MAX - imm2
                        sign3 = imm3 & MSB
                        if sign3:
                            imm3 = MAX - imm3
                        sign = sign2 ^ sign3
                        
                        number = imm2 // imm3
                        if sign:
                            number = MAX - number
                        
                        answer = ["IMM", line[1], str(number)]
                        
                    case "SBRL":
                        if (imm2 ^ MSB) < (imm3 ^ MSB):
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "SBRG":
                        if (imm2 ^ MSB) > (imm3 ^ MSB):
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]

                    case "SBLE":
                        if (imm2 ^ MSB) <= (imm3 ^ MSB):
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                            
                    case "SBGE":
                        if (imm2 ^ MSB) >= (imm3 ^ MSB):
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                            
                    case "SSETL":
                        if (imm2 ^ MSB) < (imm3 ^ MSB):
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]

                    case "SSETG":
                        if (imm2 ^ MSB) > (imm3 ^ MSB):
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                    
                    case "SSETLE":
                        if (imm2 ^ MSB) <= (imm3 ^ MSB):
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                            
                    case "SSETGE":
                        if (imm2 ^ MSB) >= (imm3 ^ MSB):
                            answer = ["IMM", line[1], str(MAX)]
                        else:
                            answer = ["IMM", line[1], "0"]
                    
                code[index] = answer.copy()
                success = True

        elif line[0] in imm2Only:
            if line[2][0: ].isnumeric():
                imm2 = int(line[2], 0)
                
                answer = [f"Unrecognised Instruction: {line[0]}"]
                match line[0]:
                    case "RSH":
                        number = imm2 >> 1
                        answer = ["IMM", line[1], str(number)]
                    
                    case "LSH":
                        number = (imm2 << 1) & MAX
                        answer = ["IMM", line[1], str(number)]
                    
                    case "INC":
                        number = (imm2 + 1) & MAX
                        answer = ["IMM", line[1], str(number)]

                    case "DEC":
                        number = (imm2 + MAX) & MAX
                        answer = ["IMM", line[1], str(number)]

                    case "NEG":
                        number = (MAX - imm2 + 1) & MAX
                        answer = ["IMM", line[1], str(number)]

                    case "NOT":
                        number = MAX - imm2
                        answer = ["IMM", line[1], str(number)]

                    case "BOD":
                        if imm2 & 1:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                            
                    case "BEV":
                        if 1 - (imm2 & 1):
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "BRZ":
                        if imm2:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]

                    case "BNZ":
                        if imm2 != 0:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                            
                    case "BRN":
                        if imm2 >= MSB:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "BRP":
                        if imm2 < MSB:
                            answer = ["JMP", line[1]]
                        else:
                            answer = [""]
                    
                    case "SRS":
                        if imm2 & MSB:
                            number = MSB
                        number += (imm2 >> 1)
                    
                        answer = ["IMM", line[1], str(number)]
                    
                    case "ABS":
                        if imm2 & MSB:
                            number = MAX - imm2
                        else:
                            number = imm2
                        
                        answer = ["IMM", line[1], str(number)]
                
                code[index] = answer.copy()
                success = True

    code, success2 = removeEmptyLines(code)
    success |= success2
    
    return code, success

### Immediate Folding (not fully solvable instructions with an immediate)
def partialImmediateFolding(code: list, BITS: int):
    
    success = False
    
    optimisableInstructions = (
        "ADD",
        "BGE",
        "NOR",
        "SUB",
        "AND",
        "OR",
        "XNOR",
        "XOR",
        "NAND",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BLE",
        "BRC",
        "BNC",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
        "BSS",
        "SETE",
        "SETNE",
        "SETG",
        "SETL",
        "SETGE",
        "SETLE",
        "SETC",
        "SETNC",
        "SDIV",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE",
        "SSETL",
        "SSETG",
        "SSETLE",
        "SSETGE"
    )

    MAX = 2**BITS - 1
    MSB = 2**(BITS - 1)

    for index, line in enumerate(code):
        if line[0] in optimisableInstructions:
            imm2 = ""
            imm3 = ""
            if line[2][0: ].isnumeric():
                imm2 = int(line[2], 0)
            if line[3][0: ].isnumeric():
                imm3 = int(line[3], 0)

            answer = ""
            match line[0]:
                case "ADD":
                    if imm2 == 0:
                        answer = ["MOV", line[1], line[3]]
                    elif imm3 == 0:
                        answer = ["MOV", line[1], line[2]]
                    elif imm2 == 1:
                        answer = ["INC", line[1], line[3]]
                    elif imm3 == 1:
                        answer = ["INC", line[1], line[2]]
                    elif imm2 == MAX:
                        answer = ["DEC", line[1], line[3]]
                    elif imm3 == MAX:
                        answer = ["DEC", line[1], line[2]]
                    
                case "BGE":
                    if imm2 == 0:
                        answer = ["BRZ", line[1], line[3]]
                    elif imm2 == MAX:
                        answer = ["JMP", line[1]]
                    elif imm3 == 0:
                        answer = ["JMP", line[1]]
                    elif imm3 == 1:
                        answer = ["BNZ", line[1], line[2]]
                
                case "NOR":
                    if imm2 == 0:
                        answer = ["NOT", line[1], line[3]]
                    elif (imm2 == MAX) or (imm3 == MAX):
                        answer = ["IMM", line[1], "0"]
                    elif imm3 == 0:
                        answer = ["NOT", line[1], line[2]]
                
                case "SUB":
                    if imm2 == 0:
                        answer = ["NEG", line[1], line[3]]
                    elif imm2 == MAX:
                        answer = ["NOT", line[1], line[3]]
                    elif imm3 == 0:
                        answer = ["MOV", line[1], line[2]]
                    elif imm3 == 1:
                        answer = ["DEC", line[1], line[2]]
                    elif imm3 == MAX:
                        answer = ["INC", line[1], line[2]]
                
                case "AND":
                    if (imm2 == 0) or (imm3 == 0):
                        answer = ["IMM", line[1], "0"]
                    elif imm2 == MAX:
                        answer = ["MOV", line[1], line[3]]
                    elif imm3 == MAX:
                        answer = ["MOV", line[1], line[2]]
                
                case "OR":
                    if imm2 == 0:
                        answer = ["MOV", line[1], line[3]]
                    elif (imm2 == MAX) or (imm3 == MAX):
                        answer = ["IMM", line[1], str(MAX)]
                    elif imm3 == 0:
                        answer = ["MOV", line[1], line[2]]
                
                case "XNOR":
                    if imm2 == 0:
                        answer = ["NOT", line[1], line[3]]
                    elif imm2 == MAX:
                        answer = ["MOV", line[1], line[3]]
                    elif imm3 == 0:
                        answer = ["NOT", line[1], line[2]]
                    elif imm3 == MAX:
                        answer = ["MOV", line[1], line[2]]
                
                case "XOR":
                    if imm2 == 0:
                        answer = ["MOV", line[1], line[3]]
                    elif imm2 == MAX:
                        answer = ["NOT", line[1], line[3]]
                    elif imm3 == 0:
                        answer = ["MOV", line[1], line[2]]
                    elif imm3 == MAX:
                        answer = ["NOT", line[1], line[2]]
                
                case "NAND":
                    if (imm2 == 0) or (imm3 == 0):
                        answer = ["IMM", line[1], str(MAX)]
                    elif imm2 == MAX:
                        answer = ["NOT", line[1], line[3]]
                    elif imm3 == MAX:
                        answer = ["NOT", line[1], line[2]]
                        
                case "BRL":
                    if imm2 == 0:
                        answer = ["BNZ", line[1], line[3]]
                    elif imm2 == MAX:
                        answer = [""]
                    elif imm3 == 0:
                        answer = [""]
                        
                case "BRG":
                    if imm3 == 0:
                        answer = ["BNZ", line[1], line[2]]
                    elif imm3 == MAX:
                        answer = [""]
                    elif imm2 == 0:
                        answer = [""]
                
                case "BRE":
                    if imm2 == 0:
                        answer = ["BRZ", line[1], line[3]]
                    elif imm3 == 0:
                        answer = ["BRZ", line[1], line[2]]
                
                case "BNE":
                    if imm2 == 0:
                        answer = ["BNZ", line[1], line[3]]
                    elif imm3 == 0:
                        answer = ["BNZ", line[1], line[2]]
                
                case "BLE":
                    if (imm2 == 0) or (imm3 == MAX):
                        answer = ["JMP", line[1]]
                    elif imm3 == 0:
                        answer = ["BRZ", line[1], line[2]]
                        
                case "BRC":
                    if (imm2 == 0) or (imm3 == 0):
                        answer = [""]
                    elif imm2 == MAX:
                        answer = ["BNZ", line[1], line[3]]
                    elif imm3 == MAX:
                        answer = ["BNZ", line[1], line[2]]
                
                case "BNC":
                    if (imm2 == 0) or (imm3 == 0):
                        answer = ["JMP", line[1]]
                    elif imm2 == MAX:
                        answer = ["BRZ", line[1], line[3]]
                    elif imm3 == MAX:
                        answer = ["BRZ", line[1], line[2]]
                
                case "MLT":
                    if type(imm2) == int:
                        if (imm2 == 0) or (imm3 == 0):
                            answer = ["IMM", line[1], "0"]
                        elif bin(imm2)[2: ].count("1") == 1:
                            answer = ["BSL", line[1], line[3], str(bin(imm2)[2: ].count("0"))]
                    elif type(imm3) == int:
                        if (imm2 == 0) or (imm3 == 0):
                            answer = ["IMM", line[1], "0"]
                        elif bin(imm3)[2: ].count("1") == 1:
                            answer = ["BSL", line[1], line[2], str(bin(imm3)[2: ].count("0"))]
                    else:
                        if (imm2 == 0) or (imm3 == 0):
                            answer = ["IMM", line[1], "0"]
                    
                case "DIV":
                    if type(imm3) == int:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["IMM", line[1], str(MAX)]
                        elif bin(imm3)[2: ].count("1") == 1:
                            answer = ["BSR", line[1], line[2], str(bin(imm3)[2: ].count("0"))]
                    else:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["IMM", line[1], str(MAX)]
                
                case "MOD":
                    if type(imm3) == int:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif bin(imm3)[2: ].count("1") == 1:
                            answer = ["AND", line[1], line[2], str(imm3 - 1)]
                    else:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                
                case "BSR":
                    if type(imm3) == int:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 >= BITS:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif imm3 == 1:
                            answer = ["RSH", line[1], line[2]]
                    else:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif imm3 == 1:
                            answer = ["RSH", line[1], line[2]]

                case "BSL":
                    if type(imm3) == int:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif imm3 == 1:
                            answer = ["LSH", line[1], line[2]]
                    else:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 >= BITS:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif imm3 == 1:
                            answer = ["LSH", line[1], line[2]]
                    
                case "BSS":
                    if type(imm3) == int:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm2 == MAX:
                            answer = ["IMM", line[1], str(MAX)]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif imm3 == 1:
                            answer = ["SRS", line[1], line[2]]
                        elif imm3 >= BITS:
                            answer = ["IMM", line[1], str(MAX)]
                    else:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm2 == MAX:
                            answer = ["IMM", line[1], str(MAX)]
                        elif imm3 == 0:
                            answer = ["MOV", line[1], line[2]]
                        elif imm3 == 1:
                            answer = ["SRS", line[1], line[2]]
                
                case "SETE":
                    pass
                    
                case "SETNE":
                    pass
                
                case "SETG":
                    if imm2 == 0:
                        answer = ["IMM", line[1], "0"]
                    elif imm3 == MAX:
                        answer = ["IMM", line[1], "0"]
                
                case "SETL":
                    if imm3 == MAX:
                        answer = ["IMM", line[1], "0"]
                    elif imm2 == 0:
                        answer = ["IMM", line[1], "0"]
                
                case "SETGE":
                    if imm2 == MAX:
                        answer = ["IMM", line[1], str(MAX)]
                    elif imm3 == 0:
                        answer = ["IMM", line[1], str(MAX)]
                    
                case "SETLE":
                    if imm3 == MAX:
                        answer = ["IMM", line[1], str(MAX)]
                    elif imm2 == 0:
                        answer = ["IMM", line[1], str(MAX)]
                    
                case "SETC":
                    if (imm2 == 0) or (imm3 == 0):
                        answer = ["IMM", line[1], "0"]
                
                case "SETNC":
                    if (imm2 == 0) or (imm3 == 0):
                        answer = ["IMM", line[1], str(MAX)]
                
                case "SDIV":
                    if type(imm3) == int:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = (
                                ["BSS", line[1], line[2], str(BITS)],
                                ["NOT", line[1], line[1]]
                                )
                        elif (imm3 < MSB) and (bin(imm3)[2: ].count("1") == 1):
                            answer = ["BSS", line[1], str(bin(imm3)[2: ].count("0"))]
                    else:
                        if imm2 == 0:
                            answer = ["IMM", line[1], "0"]
                        elif imm3 == 0:
                            answer = (
                                ["BSS", line[1], line[2], str(BITS)],
                                ["NOT", line[1], line[1]]
                                )
                    
                case "SBRL":
                    if type(imm2) == int:
                        if imm2 ^ MSB == 0:
                            answer = ["BNE", line[1], line[3], str(MSB)]
                        elif imm2 ^ MSB == MAX:
                            answer = [""]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = [""]
                        
                case "SBRG":
                    if type(imm2) == int:
                        if imm2 ^ MSB == 0:
                            answer = [""]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["BNE", line[1], line[2], str(MSB)]
                        elif imm3 ^ MSB == MAX:
                            answer = [""]
                
                case "SBLE":
                    if type(imm2) == int:
                        if (imm2 ^ MSB == 0) or (imm3 ^ MSB == MAX):
                            answer = ["JMP", line[1]]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["BRE", line[1], line[2], str(MSB)]
                        
                case "SBGE":
                    if type(imm2) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["JMP", line[1]]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["JMP", line[1]]
                    
                case "SSETL":
                    if type(imm2) == int:
                        if imm2 ^ MSB == 0:
                            answer = ["SETNE", line[1], line[3], str(MSB)]
                        elif imm2 ^ MSB == MAX:
                            answer = ["IMM", line[0], "0"]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["IMM", line[0], "0"]
                    
                case "SSETG":
                    if type(imm2) == int:
                        if imm2 ^ MSB == 0:
                            answer = ["IMM", line[0], "0"]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["SETNE", line[1], line[2], str(MSB)]
                        elif imm3 ^ MSB == MAX:
                            answer = ["IMM", line[0], "0"]
                
                case "SSETLE":
                    if type(imm2) == int:
                        if imm3 ^ MSB == MAX:
                            answer = ["IMM", line[1], str(MAX)]
                        elif imm3 ^ MSB == 0:
                            answer = ["SETE", line[1], line[2], str(MSB)]
                    elif type(imm3) == int:
                        if imm2 ^ MSB == 0:
                            answer = ["IMM", line[1], str(MAX)]
                    
                case "SSETGE":
                    if type(imm2) == int:
                        if imm2 ^ MSB == MAX:
                            answer = ["IMM", line[1], str(MAX)]
                        elif imm2 ^ MSB == 0:
                            answer = ["SETE", line[1], line[3], str(MSB)]
                    elif type(imm3) == int:
                        if imm3 ^ MSB == 0:
                            answer = ["IMM", line[1], str(MAX)]
                    
            if type(answer) == list:
                code[index] = answer.copy()
                success = True
            elif type(answer) == tuple:
                code[: index] + list(answer) + code[index + 1: ]
                success = True
                break
    
    code, success2 = removeEmptyLines(code)
    success |= success2
    
    return code, success

### Immediate Folding (no immediate values)
def noImmediateFolding(code: list, BITS: int):
    
    success = False
    
    optimisableInstructions = (
        "ADD",
        "BGE",
        "NOR",
        "SUB",
        "AND",
        "OR",
        "XNOR",
        "XOR",
        "NAND",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BLE",
        "BRC",
        "BNC",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
        "BSS",
        "SETE",
        "SETNE",
        "SETG",
        "SETL",
        "SETGE",
        "SETLE",
        "SETC",
        "SETNC",
        "SDIV",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE",
        "SSETL",
        "SSETG",
        "SSETLE",
        "SSETGE"
    )

    MAX = 2**BITS - 1
    MSB = 2**(BITS - 1)

    for index, line in enumerate(code):
        if line[0] in optimisableInstructions:
            if line[2] == line[3]:
            
                answer = [f"Unrecognised Instruction: {line[0]}"]
                match line[0]:
                    case "ADD":
                        answer = ["LSH", line[1], line[2]]
                    
                    case "BGE":
                        answer = ["JMP", line[1]]
                        
                    case "NOR":
                        answer = ["NOT", line[1], line[2]]
                        
                    case "SUB":
                        answer = ["IMM", line[1], "0"]
                        
                    case "AND":
                        answer = ["MOV", line[1], line[2]]
                        
                    case "OR":
                        answer = ["MOV", line[1], line[2]]
                        
                    case "XNOR":
                        answer = ["IMM", line[1], str(MAX)]
                        
                    case "XOR":
                        answer = ["IMM", line[1], "0"]
                        
                    case "NAND":
                        answer = ["NOT", line[1], line[2]]
                        
                    case "BRL":
                        answer = [""]
                        
                    case "BRG":
                        answer = [""]
                        
                    case "BRE":
                        answer = ["JMP", line[1]]
                        
                    case "BNE":
                        answer = [""]
                        
                    case "BLE":
                        answer = ["JMP", line[1]]
                        
                    case "BRC":
                        answer = ["BRN", line[1], line[2]]
                        
                    case "BNC":
                        answer = ["BRP", line[1], line[2]]
                        
                    case "MLT":
                        pass
                        
                    case "DIV":
                        answer = ["IMM", line[1], "1"]
                        
                    case "MOD":
                        answer = ["IMM", line[1], "0"]
                        
                    case "BSR":
                        answer = ["IMM", line[1], "0"]
                        
                    case "BSL":
                        pass
                        
                    case "BSS":
                        pass
                        
                    case "SETE":
                        answer = ["IMM", line[1], str(MAX)]
                        
                    case "SETNE":
                        answer = ["IMM", line[1], "0"]
                        
                    case "SETG":
                        answer = ["IMM", line[1], "0"]
                        
                    case "SETL":
                        answer = ["IMM", line[1], "0"]
                        
                    case "SETGE":
                        answer = ["IMM", line[1], str(MAX)]
                        
                    case "SETLE":
                        answer = ["IMM", line[1], str(MAX)]
                        
                    case "SETC":
                        pass
                        
                    case "SETNC":
                        pass
                        
                    case "SDIV":
                        answer = ["IMM", line[1], "1"]
                        
                    case "SBRL":
                        answer = [""]
                        
                    case "SBRG":
                        answer = [""]
                        
                    case "SBLE":
                        answer = ["JMP", line[1]]
                        
                    case "SBGE":
                        answer = ["JMP", line[1]]
                        
                    case "SSETL":
                        answer = ["IMM", line[1], "0"]
                        
                    case "SSETG":
                        answer = ["IMM", line[1], "0"]
                        
                    case "SSETLE":
                        answer = ["IMM", line[1], str(MAX)]
                        
                    case "SSETGE":
                        answer = ["IMM", line[1], str(MAX)]
                    
                code[index] = answer
                success = True
                
    code, success2 = removeEmptyLines(code)
    success |= success2
    
    return code, success

### Immediate Propagation
def immediatePropagation(code: list):
    
    success = False
    
    read2and3 = (
        "ADD",
        "NOR",
        "SUB",
        "AND",
        "OR",
        "XNOR",
        "XOR",
        "NAND",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
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
        "SSETGE"
    )
    
    read2 = (
        "RSH",
        "LOD",
        "MOV",
        "LSH",
        "INC",
        "DEC",
        "NEG",
        "NOT",
        "SRS",
        "ABS",
        "OUT"
    )
    
    read1and2and3 = (
        "BGE",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BLE",
        "BRC",
        "BNC",
        "LSTR",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE"
    )
    
    read1 = (
        "JMP",
        "PSH",
        "CAL"
    )
    
    read1and2 = (
        "STR",
        "BOD",
        "BEV",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "CPY"
    )
    
    write1 = (
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
        "POP",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
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
        "ABS",
        "IN"
    )
    
    for index, line in enumerate(code):
        if line[0] == "IMM":
            key = line[1]
            definition = line[2]
            for index2, line2 in enumerate(code[index + 1: ]):
                
                if line2[0].startswith("."):
                    break
                
                elif line2[0] in read2and3:
                    if line2[2] == key:
                        code[index + 1 + index2][2] = definition
                        success = True
                    if line2[3] == key:
                        code[index + 1 + index2][3] = definition
                        success = True
                    
                    if line2[0] in write1:
                        if line2[1] == key:
                            break
                    
                elif line2[0] in read2:
                    if line2[2] == key:
                        code[index + 1 + index2][2] = definition
                        success = True
                        
                    if line2[0] in write1:
                        if line2[1] == key:
                            break
                    
                elif line2[0] in read1and2and3:
                    if line2[1] == key:
                        code[index + 1 + index2][1] = definition
                        success = True
                    if line2[2] == key:
                        code[index + 1 + index2][2] = definition
                        success = True
                    if line2[3] == key:
                        code[index + 1 + index2][3] = definition
                        success = True
                        
                elif line2[0] in read1:
                    if line2[1] == key:
                        code[index + 1 + index2][1] = definition
                        success = True
                
                elif line2[0] in read1and2:
                    if line2[1] == key:
                        code[index + 1 + index2][1] = definition
                        success = True
                    if line2[2] == key:
                        code[index + 1 + index2][2] = definition
                        success = True
                    
                else:
                    if line2[0] in write1:
                        if line2[1] == key:
                            break
                            
    return code, success

### Write Before Read
def writeBeforeRead(code: list):
    
    success = False
    
    read2and3 = (
        "ADD",
        "NOR",
        "SUB",
        "AND",
        "OR",
        "XNOR",
        "XOR",
        "NAND",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
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
        "SSETGE"
    )
    
    read2 = (
        "RSH",
        "LOD",
        "MOV",
        "LSH",
        "INC",
        "DEC",
        "NEG",
        "NOT",
        "SRS",
        "ABS",
        "OUT"
    )
    
    read1and2and3 = (
        "BGE",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BLE",
        "BRC",
        "BNC",
        "LSTR",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE"
    )
    
    read1 = (
        "JMP",
        "PSH",
        "CAL"
    )
    
    read1and2 = (
        "STR",
        "BOD",
        "BEV",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "CPY"
    )
    
    write1 = (
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
        "POP",
        "MLT",
        "DIV",
        "MOD",
        "BSR",
        "BSL",
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
        "ABS",
        "IN"
    )
    
    branches = (
        "JMP",
        "BRL",
        "BRG",
        "BRE",
        "BNE",
        "BOD",
        "BEV",
        "BLE",
        "BRZ",
        "BNZ",
        "BRN",
        "BRP",
        "CAL",
        "RET",
        "HLT",
        "SBRL",
        "SBRG",
        "SBLE",
        "SBGE"
    )
    
    for index, line in enumerate(code):
        if line[0] in write1:
            writeTarget = line[1]
            for index2, line2 in enumerate(code[index + 1: ]):
                if line2[0] in branches:
                    break
                
                elif line2[0] in read2and3:
                    if line2[2] == writeTarget:
                        break
                    if line2[3] == writeTarget:
                        break
                
                elif line2[0] in read2:
                    if line2[2] == writeTarget:
                        break
                
                elif line2[0] in read1and2and3:
                    if line2[1] == writeTarget:
                        break
                    if line2[2] == writeTarget:
                        break
                    if line2[3] == writeTarget:
                        break
                    
                elif line2[0] in read1:
                    if line2[1] == writeTarget:
                        break
                
                elif line2[0] in read1and2:
                    if line2[1] == writeTarget:
                        break
                    if line2[2] == writeTarget:
                        break
                
                if line2[0] in write1:
                    if line2[1] == "PC":
                        break
                
                    elif line2[1] == writeTarget:
                        code[index] = [""]
                        success = True
    
    return code, success

### Detect OUT Instructions
def detectOUT(code: list):
    
    success = False
    
    for line in code:
        if line[0] == "OUT":
            return code, success

    return [], success

### Inline Branches
def inlineBranches(code: list):
    
    success = False
    
    for index, line in enumerate(code):
        if line[0].startswith("."):
            label = line[0]
            
            pointer1 = index
            pointer2 = pointer1 + 1
            bad = False
            while pointer2 < len(code):
                if code[pointer2][0].startswith("."):
                    bad = True
                    break
                elif code[pointer2][0] in ("JMP", "HLT", "RET"):
                    pointer2 += 1
                    break
                else:
                    pointer2 += 1
            
            if not bad:
                codeBlock = code[pointer1: pointer2]
                code2 = code[: pointer1] + code[pointer2: ]
                
                # find if label is unique to one JMP in code2
                
                count = 0
                target = ""
                for index2, line2 in enumerate(code2):
                    if (line2.count(label)) and (line2[0] != "JMP"):
                        count = 2
                        break
                    elif line2.count(label):
                        target = index2

                    count += line2.count(label)
                
                if count == 1:
                    code = code2[: target] + codeBlock + code2[target + 1: ]

                    success = True
                    
                    return inlineBranches(code)[0], success
            
    return code, success





