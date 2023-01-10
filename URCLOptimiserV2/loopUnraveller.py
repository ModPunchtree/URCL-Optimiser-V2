
from copy import deepcopy

def loopUnraveller(codeBlock__: list, BITS: int, REGTotal: int, HEAPTotal: int, cycleLimit = 500, M0 = -1):
    
    if not codeBlock__:
        raise Exception("no")
    
    REGTotal = 29 # this is to make SP work
    
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
        "HPSH",
        "CAL",
        "HCAL",
        "HSAV"
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
        "IN",
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
        "HPOP",
        "HRSR",
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
    
    codeBlock_ = deepcopy(codeBlock__)

    MAX = 2**BITS - 1
    MSB = 2**(BITS - 1)

    # convert labels to immediates
    codeBlock = []
    labels = []
    labelValues = []
    index = 0
    while index < len(codeBlock_):
        line = codeBlock_[index]
        if line[0].startswith("."):
            labels.append(line[0])
            labelValues.append(str(index))
            codeBlock_.pop(index)
        else:
            codeBlock.append(line)
            index += 1
    for index, line in enumerate(codeBlock):
        if line[0] in ("CAL", "RET", "PSH", "POP"):
            raise Exception("codeBlock must not contain stack instructions")
        elif line[0] == "DW":
            raise Exception("codeBlock must not contain DW values")
        for index2, token in enumerate(line):
            if token in labels:
                codeBlock[index][index2] = labelValues[labels.index(token)]
            elif token == "SP":
                codeBlock[index][index2] = "R29"
            elif token.startswith("."):
                raise Exception(f"Undefined label: {token}")

    # detect if Mx is used inappropriately or raw immediate ram addresses
    for index, line in enumerate(codeBlock):
        match line[0]:
            case "STR":
                if line[2].startswith("M") and (M0 == -1):
                    raise Exception("bad Mx usage")
                if line[1][0].isnumeric() and (M0 == -1):
                    raise Exception("immediate memory locations are unsupported")
            case "LOD":
                if line[1].startswith("M") and (M0 == -1):
                    raise Exception("bad Mx usage")
                if line[2][0].isnumeric() and (M0 == -1):
                    raise Exception("immediate memory locations are unsupported")
            case "LLOD":
                if line[1].startswith("M") and (M0 == -1):
                    raise Exception("bad Mx usage")
                if line[2].startswith("M") and line[3].startswith("M") and (M0 == -1):
                    raise Exception("bad Mx usage")
                if line[2][0].isnumeric() and line[3][0].isnumeric() and (M0 == -1):
                    raise Exception("immediate memory locations are unsupported")
            case "LSTR":
                if line[3].startswith("M") and (M0 == -1):
                    raise Exception("bad Mx usage")
                if line[1].startswith("M") and line[2].startswith("M") and (M0 == -1):
                    raise Exception("bad Mx usage")
                if line[1][0].isnumeric() and line[2][0].isnumeric() and (M0 == -1):
                    raise Exception("immediate memory locations are unsupported")
            case "CPY":
                if line[1][0].isnumeric() or line[2][0].isnumeric() and (M0 == -1):
                    raise Exception("immediate memory locations are unsupported")
            case _:
                for token in line[1: ]:
                    if token.startswith("M") and (M0 == -1):
                        raise Exception("bad Mx usage")

    # if M0 is given, replace all M prepended values with immediates
    if M0 != -1:
        for index1, line in enumerate(codeBlock):
            for index2, token in enumerate(line):
                if index2 == 0:
                    pass
                elif token.startswith("M"):
                    num = int(token[1: ], 0)
                    codeBlock[index1][index2] = f"{num + M0}"

    initialState_REG = [f"R{i}" for i in range(REGTotal + 1)]
    initialState_HEAP = [f"M{i}" for i in range(HEAPTotal)]
    callStack = []
    dataStack = []

    REG = initialState_REG.copy()
    HEAP = initialState_HEAP.copy()
    initialisedREG = [True for i in range(REGTotal + 1)]
    initialisedHEAP = [True for i in range(HEAPTotal)]
    initialisedHEAP2 = [False for i in range(HEAPTotal)]
    
    resultInstructions = []
    
    PC = 0
    branch = False
    cycles = 0
    while PC != len(codeBlock):
        
        if (len(callStack) > 32) or (len(dataStack) > 32):
            raise Exception("Hardware stacks overflowed")
        
        if cycles >= cycleLimit:
            raise Exception("Codeblock failed to halt")
        cycles += 1
        
        if (PC > len(codeBlock)) or (PC < 0):
            raise Exception("PC out of range")

        line = codeBlock[PC]
        
        instruction = line[0]
        operands = line.copy()
        
        # fetch operands (current values in registers)
        if instruction in read2and3:
            if line[2].startswith("R"):
                index = int(line[2][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[2] = str(REG[index])
            if line[3].startswith("R"):
                index = int(line[3][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[3] = str(REG[index])
                
        elif instruction in read2:
            if line[2].startswith("R"):
                index = int(line[2][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[2] = str(REG[index])
        
        elif instruction in read1and2and3:
            if line[1].startswith("R"):
                index = int(line[1][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[1] = str(REG[index])
            if line[2].startswith("R"):
                index = int(line[2][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[2] = str(REG[index])
            if line[3].startswith("R"):
                index = int(line[3][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[3] = str(REG[index])

        elif instruction in read1:
            if line[1].startswith("R"):
                index = int(line[1][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[1] = str(REG[index])
        
        elif instruction in read1and2:
            if line[1].startswith("R"):
                index = int(line[1][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[1] = str(REG[index])
            if line[2].startswith("R"):
                index = int(line[2][1: ], 0)
                if not initialisedREG[index]:
                    raise Exception("read before write")
                operands[2] = str(REG[index])
        
        # fetch operands (current value in the heap)
        if instruction == "LOD":
            if operands[2].startswith("M"):
                operands[2] = str(HEAP[int(operands[2][1: ], 0)])
            elif operands[2][0].isnumeric():
                operands[2] = str(HEAP[int(operands[2], 0)])
            else:
                raise Exception("Invalid LOD location")
        elif instruction == "LLOD":
            if operands[2].startswith("M") and operands[3][0].isnumeric():
                instruction = "LOD"
                operands[2] = str(HEAP[int(operands[2][1: ], 0) + int(operands[3], 0)])
                operands.pop(3)
            elif operands[2][0].isnumeric() and operands[3][0].isnumeric():
                instruction = "LOD"
                operands[2] = str(HEAP[int(operands[2], 0) + int(operands[3], 0)])
                operands.pop(3)
            elif operands[3].startswith("M") and operands[2][0].isnumeric():
                instruction = "LOD"
                operands[2] = str(HEAP[int(operands[2], 0) + int(operands[3][1: ], 0)])
                operands.pop(3)
            else:
                raise Exception("oppsie")
        
        # calculate instruction result
        match instruction:
            case "ADD":
                resultInstructions.append(line.copy())
                try:
                    answer = (int(operands[2], 0) + int(operands[3], 0)) & MAX
                except Exception as x:
                    answer = "?"
            case "RSH":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) // 2
                except Exception as x:
                    answer = "?"
            case "LOD":
                resultInstructions.append(line.copy())
                answer = operands[2]
            case "STR":
                resultInstructions.append(line.copy())
                answer = operands[2]
            case "BGE":
                answer = int(operands[2], 0) >= int(operands[3], 0)
            case "NOR":
                resultInstructions.append(line.copy())
                try:
                    answer = MAX - (int(operands[2], 0) | int(operands[3], 0))
                except Exception as x:
                    answer = "?"
            case "SUB":
                resultInstructions.append(line.copy())
                try:
                    answer = (int(operands[2], 0) + (MAX - int(operands[3], 0)) + 1) & MAX
                except Exception as x:
                    answer = "?"
            case "JMP":
                answer = True
            case "MOV":
                resultInstructions.append(line.copy())
                answer = operands[2]
            case "IN":
                resultInstructions.append(line.copy())
                answer = line[1]
            case "IMM":
                resultInstructions.append(line.copy())
                answer = operands[2]
            case "LSH":
                resultInstructions.append(line.copy())
                try:
                    answer = (int(operands[2], 0) * 2) & MAX
                except Exception as x:
                    answer = "?"
            case "INC":
                resultInstructions.append(line.copy())
                try:
                    answer = (int(operands[2], 0) + 1) & MAX
                except Exception as x:
                    answer = "?"
            case "DEC":
                resultInstructions.append(line.copy())
                try:
                    answer = (int(operands[2], 0) + MAX) & MAX
                except Exception as x:
                    answer = "?"
            case "NEG":
                resultInstructions.append(line.copy())
                try:
                    answer = ((MAX - int(operands[2], 0)) + 1) & MAX
                except Exception as x:
                    answer = "?"
            case "AND":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) & int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "OR":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) | int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "NOT":
                resultInstructions.append(line.copy())
                try:
                    answer = MAX - int(operands[2], 0)
                except Exception as x:
                    answer = "?"
            case "XNOR":
                resultInstructions.append(line.copy())
                try:
                    answer = MAX - (int(operands[2], 0) ^ int(operands[3], 0))
                except Exception as x:
                    answer = "?"
            case "XOR":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) ^ int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "NAND":
                resultInstructions.append(line.copy())
                try:
                    answer = MAX - (int(operands[2], 0) & int(operands[3], 0))
                except Exception as x:
                    answer = "?"
            case "BRL":
                answer = int(operands[2], 0) < int(operands[3], 0)
            case "BRG":
                answer = int(operands[2], 0) > int(operands[3], 0)
            case "BRE":
                answer = operands[2] == operands[3]
            case "BNE":
                answer = operands[2] != operands[3]
            case "BOD":
                answer = int(operands[2], 0) & 1 == 1
            case "BEV":
                answer = int(operands[2], 0) & 1 == 0
            case "BLE":
                answer = int(operands[2], 0) <= int(operands[3], 0)
            case "BRZ":
                if operands[2][0].isnumeric():
                    answer = int(operands[2], 0) == 0
                elif operands[2].startswith("'"):
                    answer = False
                else:
                    raise Exception("Bad")
            case "BNZ":
                if operands[2][0].isnumeric():
                    answer = int(operands[2], 0) != 0
                elif operands[2].startswith("'"):
                    answer = True
                else:
                    raise Exception("Bad")
            case "BRN":
                answer = int(operands[2], 0) & MSB != 0
            case "BRP":
                answer = int(operands[2], 0) & MSB == 0
            case "HLT":
                # bad
                raise Exception("Must not contain HLT")
            case "CPY":
                resultInstructions.append(line.copy())
                answer = operands[2]
            case "BRC":
                answer = (int(operands[2], 0) + int(operands[3], 0)) > MAX
            case "BNC":
                answer = (int(operands[2], 0) + int(operands[3], 0)) <= MAX
            case "MLT":
                resultInstructions.append(line.copy())
                try:
                    answer = (int(operands[2], 0) * int(operands[3], 0)) & MAX
                except Exception as x:
                    answer = "?"
            case "UMLT":
                resultInstructions.append(line.copy())
                try:
                    answer = ((int(operands[2], 0) * int(operands[3], 0)) & (MAX << BITS)) >> BITS
                except Exception as x:
                    answer = "?"
            case "DIV":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) // int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "MOD":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) % int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "BSR":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) >> int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "BSL":
                resultInstructions.append(line.copy())
                try:
                    answer = int(operands[2], 0) << int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "SRS":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) & MSB:
                        answer = (int(operands[2], 0) >> 1) + MSB
                    else:
                        answer = int(operands[2], 0) >> 1
                except Exception as x:
                    answer = "?"
            case "BSS":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) & MSB:
                        answer = (int(operands[2], 0) >> int(operands[3], 0)) + ((2**BITS) - ((2**BITS) >> int(operands[3], 0)))
                    else:
                        answer = int(operands[2], 0) >> int(operands[3], 0)
                except Exception as x:
                    answer = "?"
            case "SETE":
                resultInstructions.append(line.copy())
                try:
                    if operands[2] == operands[3]:
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETNE":
                resultInstructions.append(line.copy())
                try:
                    if operands[2] != operands[3]:
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETG":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) > int(operands[3], 0):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETL":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) < int(operands[3], 0):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETGE":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) >= int(operands[3], 0):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETLE":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) <= int(operands[3], 0):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETC":
                resultInstructions.append(line.copy())
                try:
                    if (int(operands[2], 0) + int(operands[3], 0)) > MAX:
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SETNC":
                resultInstructions.append(line.copy())
                try:
                    if (int(operands[2], 0) + int(operands[3], 0)) <= MAX:
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "LSTR":
                resultInstructions.append(line.copy())
                answer = operands[3]
            case "SDIV":
                resultInstructions.append(line.copy())
                try:
                    op2 = int(operands[2], 0)
                    sign2 = 0
                    if op2 & MSB:
                        sign2 = 1
                        op2 = ((MAX - op2) + 1) & MAX
                    op3 = int(operands[3], 0)
                    sign3 = 0
                    if op3 & MSB:
                        sign3 = 1
                        op3 = ((MAX - op3) + 1) & MAX
                    answer = op2 // op3
                    if sign2 ^ sign3:
                        answer = ((MAX - answer) + 1) & MAX
                except Exception as x:
                    answer = "?"
            case "SBRL":
                try:
                    answer = (int(operands[2], 0) ^ MSB) < (int(operands[3], 0) ^ MSB)
                except Exception as x:
                    answer = "?"
            case "SBRG":
                try:
                    answer = (int(operands[2], 0) ^ MSB) > (int(operands[3], 0) ^ MSB)
                except Exception as x:
                    answer = "?"
            case "SBLE":
                try:
                    answer = (int(operands[2], 0) ^ MSB) <= (int(operands[3], 0) ^ MSB)
                except Exception as x:
                    answer = "?"
            case "SBGE":
                try:
                    answer = (int(operands[2], 0) ^ MSB) >= (int(operands[3], 0) ^ MSB)
                except Exception as x:
                    answer = "?"
            case "SSETL":
                resultInstructions.append(line.copy())
                try:
                    if (int(operands[2], 0) ^ MSB) < (int(operands[3], 0) ^ MSB):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SSETG":
                resultInstructions.append(line.copy())
                try:
                    if (int(operands[2], 0) ^ MSB) > (int(operands[3], 0) ^ MSB):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SSETLE":
                resultInstructions.append(line.copy())
                try:
                    if (int(operands[2], 0) ^ MSB) <= (int(operands[3], 0) ^ MSB):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "SSETGE":
                resultInstructions.append(line.copy())
                try:
                    if (int(operands[2], 0) ^ MSB) >= (int(operands[3], 0) ^ MSB):
                        answer = MAX
                    else:
                        answer = 0
                except Exception as x:
                    answer = "?"
            case "ABS":
                resultInstructions.append(line.copy())
                try:
                    if int(operands[2], 0) & MSB:
                        answer = ((MAX - int(operands[2], 0)) + 1) & MAX
                    else:
                        answer = int(operands[2], 0)
                except Exception as x:
                    answer = "?"
            case "IN":
                resultInstructions.append(line.copy())
            case "OUT":
                resultInstructions.append(line.copy())
                answer = operands[2]
            case "HPSH":
                resultInstructions.append(line.copy())
                answer = "HPSH"
            case "HPOP":
                resultInstructions.append(line.copy())
                try:
                    answer = dataStack.pop()
                except Exception as x:
                    answer = "?"
            case "HCAL":
                resultInstructions.append(line.copy())
                answer = "HCAL"
            case "HRET":
                resultInstructions.append(line.copy())
                answer = callStack.pop()
            case "HSAV":
                resultInstructions.append(line.copy())
                answer = "HSAV"
            case "HRSR":
                resultInstructions.append(line.copy())
                try:
                    answer = dataStack.pop()
                except Exception as x:
                    answer = "?"
            case _:
                raise Exception(f"Unrecognised instruction: {instruction}")

        # writeback
        if instruction in write1:
            REG[int(operands[1][1: ], 0)] = answer
            initialisedREG[int(operands[1][1: ], 0)] = True
        elif instruction == "STR":
            try:
                HEAP[int(operands[1], 0)] = answer
                initialisedHEAP2[int(operands[1], 0)] = True
            except:
                HEAP[int(operands[1][1: ], 0)] = answer
                initialisedHEAP2[int(operands[1][1: ], 0)] = True
        elif instruction == "LSTR":
            if operands[1].startswith("M"):
                HEAP[int(operands[1][1: ], 0) + int(operands[2], 0)] = answer
                initialisedHEAP2[int(operands[1][1: ], 0) + int(operands[2], 0)] = True
            elif operands[2].startswith("M"):
                HEAP[int(operands[1], 0) + int(operands[2][1: ], 0)] = answer
                initialisedHEAP2[int(operands[1], 0) + int(operands[2][1: ], 0)] = True
            else:
                HEAP[int(operands[1], 0) + int(operands[2], 0)] = answer
                initialisedHEAP2[int(operands[1], 0) + int(operands[2], 0)] = True
        elif instruction == "CPY":
            try:
                HEAP[int(operands[1][1: ], 0)] = answer
                initialisedHEAP2[int(operands[1][1: ], 0)] = True
            except:
                HEAP[int(operands[1], 0)] = answer
                initialisedHEAP2[int(operands[1], 0)] = True
        elif instruction in branches:
            if answer:
                PC = int(operands[1], 0)
                branch = True
        elif instruction == "OUT":
            pass
        elif instruction == "HLT":
            appendHLT = True
            break
        elif instruction == "HPSH":
            dataStack.append(int(operands[1], 0))
        elif instruction == "HCAL":
            callStack.append(PC + 1)
            PC = int(operands[1], 0)
            branch = True
        elif instruction == "HSAV":
            dataStack.append(int(operands[1], 0))
        elif instruction == "HRET":
            PC = answer
            branch = True
        elif instruction == "IN":
            pass
        else:
            raise Exception(f"Unhandled writeback instruction: {instruction}")

        if not branch:
            PC += 1
        else:
            branch = False

        REG[0] = 0 # make sure R0 always equals 0

    # leftover callstack values
    if callStack:
        raise Exception("Callstack cannot have values leftover")

    # generate result
    # fix heapLocations in resultInstructions
    for index, line in enumerate(resultInstructions):
        if line[0] == "STR":
            if line[1].isnumeric():
                resultInstructions[index][1] = f"M{int(line[1]) + M0}"
                
    if (cycles <= len(resultInstructions)):
        raise Exception("Optimised code is worse than the initial codeblock")
    
    # convert R29 back into SP
    for index, line in enumerate(resultInstructions):
        for index2, token in enumerate(line):
            if token == "R29":
                resultInstructions[index][index2] = "SP"

    return resultInstructions
