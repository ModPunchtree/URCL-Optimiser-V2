
from copy import deepcopy

def optimisationByEmulation(codeBlock__: list, BITS: int, REGTotal: int, HEAPTotal: int, cycleLimit = 500, M0 = -1):

    if not codeBlock__:
        raise Exception("no")

    REGTotal = 29 # this is to make SP work
    cycleLimit *= 2 # to compensate for increased instruction costs

    # if M0 is given, then all heap loads/stores are supported

    # no labels that point to DW values
    # no instructions that affect the stack pointer
    # no labels that point to code outside of the code block
    # no branches that go to a location outside of the code block
    # no instructions that write or read from PC
    # no instructions that read from a register or heap location that was not initialised by the code block
    # M prepended heap locations can be used to point to the heap but must never be used outside of:
        # the first operand of STR
        # the second operand of LOD
        # the second or third operands of LLOD
        # the first or second operand of LSTR
        # the first or second operand of CPY
    # Memory locations must not be specified by raw number or labels in STR, LOD, LLOD, LSTR, CPY
    
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
    
    appendHLT = False
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
        
        if PC == 120:
            stop = 1
        
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
            cycles += 1
            if operands[2].startswith("M"):
                operands[2] = str(HEAP[int(operands[2][1: ], 0)])
            elif operands[2][0].isnumeric():
                operands[2] = str(HEAP[int(operands[2], 0)])
            else:
                raise Exception("Invalid LOD location")
        elif instruction == "LLOD":
            cycles += 2
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
                answer = (int(operands[2], 0) + int(operands[3], 0)) & MAX
            case "RSH":
                answer = int(operands[2], 0) // 2
            case "LOD":
                answer = operands[2]
            case "STR":
                answer = operands[2]
            case "BGE":
                answer = int(operands[2], 0) >= int(operands[3], 0)
            case "NOR":
                answer = MAX - (int(operands[2], 0) | int(operands[3], 0))
            case "SUB":
                answer = (int(operands[2], 0) + (MAX - int(operands[3], 0)) + 1) & MAX
            case "JMP":
                answer = True
            case "MOV":
                answer = operands[2]
            case "IN":
                resultInstructions.append(line)
                answer = line[1]
            case "IMM":
                answer = operands[2]
            case "LSH":
                answer = (int(operands[2], 0) * 2) & MAX
            case "INC":
                answer = (int(operands[2], 0) + 1) & MAX
            case "DEC":
                answer = (int(operands[2], 0) + MAX) & MAX
            case "NEG":
                answer = ((MAX - int(operands[2], 0)) + 1) & MAX
            case "AND":
                answer = int(operands[2], 0) & int(operands[3], 0)
            case "OR":
                answer = int(operands[2], 0) | int(operands[3], 0)
            case "NOT":
                answer = MAX - int(operands[2], 0)
            case "XNOR":
                answer = MAX - (int(operands[2], 0) ^ int(operands[3], 0))
            case "XOR":
                answer = int(operands[2], 0) ^ int(operands[3], 0)
            case "NAND":
                answer = MAX - (int(operands[2], 0) & int(operands[3], 0))
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
                answer = True
            case "CPY":
                answer = operands[2]
            case "BRC":
                answer = (int(operands[2], 0) + int(operands[3], 0)) > MAX
            case "BNC":
                answer = (int(operands[2], 0) + int(operands[3], 0)) <= MAX
            case "MLT":
                cycles += 1
                answer = (int(operands[2], 0) * int(operands[3], 0)) & MAX
            case "UMLT":
                cycles += 1
                answer = ((int(operands[2], 0) * int(operands[3], 0)) & (MAX << BITS)) >> BITS
            case "DIV":
                cycles += 1
                answer = int(operands[2], 0) // int(operands[3], 0)
            case "MOD":
                cycles += 1
                answer = int(operands[2], 0) % int(operands[3], 0)
            case "BSR":
                answer = int(operands[2], 0) >> int(operands[3], 0)
            case "BSL":
                answer = int(operands[2], 0) << int(operands[3], 0)
            case "SRS":
                if int(operands[2], 0) & MSB:
                    answer = (int(operands[2], 0) >> 1) + MSB
                else:
                    answer = int(operands[2], 0) >> 1
            case "BSS":
                if int(operands[2], 0) & MSB:
                    answer = (int(operands[2], 0) >> int(operands[3], 0)) + ((2**BITS) - ((2**BITS) >> int(operands[3], 0)))
                else:
                    answer = int(operands[2], 0) >> int(operands[3], 0)
            case "SETE":
                if operands[2] == operands[3]:
                    answer = MAX
                else:
                    answer = 0
            case "SETNE":
                if operands[2] != operands[3]:
                    answer = MAX
                else:
                    answer = 0
            case "SETG":
                if int(operands[2], 0) > int(operands[3], 0):
                    answer = MAX
                else:
                    answer = 0
            case "SETL":
                if int(operands[2], 0) < int(operands[3], 0):
                    answer = MAX
                else:
                    answer = 0
            case "SETGE":
                if int(operands[2], 0) >= int(operands[3], 0):
                    answer = MAX
                else:
                    answer = 0
            case "SETLE":
                if int(operands[2], 0) <= int(operands[3], 0):
                    answer = MAX
                else:
                    answer = 0
            case "SETC":
                if (int(operands[2], 0) + int(operands[3], 0)) > MAX:
                    answer = MAX
                else:
                    answer = 0
            case "SETNC":
                if (int(operands[2], 0) + int(operands[3], 0)) <= MAX:
                    answer = MAX
                else:
                    answer = 0
            case "LSTR":
                answer = operands[3]
            case "SDIV":
                cycles += 3
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
            case "SBRL":
                answer = (int(operands[2], 0) ^ MSB) < (int(operands[3], 0) ^ MSB)
            case "SBRG":
                answer = (int(operands[2], 0) ^ MSB) > (int(operands[3], 0) ^ MSB)
            case "SBLE":
                answer = (int(operands[2], 0) ^ MSB) <= (int(operands[3], 0) ^ MSB)
            case "SBGE":
                answer = (int(operands[2], 0) ^ MSB) >= (int(operands[3], 0) ^ MSB)
            case "SSETL":
                if (int(operands[2], 0) ^ MSB) < (int(operands[3], 0) ^ MSB):
                    answer = MAX
                else:
                    answer = 0
            case "SSETG":
                if (int(operands[2], 0) ^ MSB) > (int(operands[3], 0) ^ MSB):
                    answer = MAX
                else:
                    answer = 0
            case "SSETLE":
                if (int(operands[2], 0) ^ MSB) <= (int(operands[3], 0) ^ MSB):
                    answer = MAX
                else:
                    answer = 0
            case "SSETGE":
                if (int(operands[2], 0) ^ MSB) >= (int(operands[3], 0) ^ MSB):
                    answer = MAX
                else:
                    answer = 0
            case "ABS":
                if int(operands[2], 0) & MSB:
                    answer = ((MAX - int(operands[2], 0)) + 1) & MAX
                else:
                    answer = int(operands[2], 0)
            case "IN":
                raise Exception("IN instructions cannot be determined")
            case "OUT":
                answer = operands[2]
            case "HPSH":
                answer = "HPSH"
            case "HPOP":
                answer = dataStack.pop()
            case "HCAL":
                answer = "HCAL"
            case "HRET":
                answer = callStack.pop()
            case "HSAV":
                answer = "HSAV"
            case "HRSR":
                answer = dataStack.pop()
            case _:
                raise Exception(f"Unrecognised instruction: {instruction}")

        # writeback
        if instruction in write1:
            REG[int(operands[1][1: ], 0)] = answer
            initialisedREG[int(operands[1][1: ], 0)] = True
        elif instruction == "STR":
            cycles += 1
            try:
                HEAP[int(operands[1], 0)] = answer
                initialisedHEAP2[int(operands[1], 0)] = True
            except:
                HEAP[int(operands[1][1: ], 0)] = answer
                initialisedHEAP2[int(operands[1][1: ], 0)] = True
        elif instruction == "LSTR":
            cycles += 2
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
            cycles += 2
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
            resultInstructions.append(["OUT", operands[1], str(answer)])
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
    for index in range(len(dataStack)):
        dataStack[index]
        resultInstructions.append(["HPSH", str(dataStack[index])])
    
    # make list of unsolved registers and heap locations
    solvedRegisters = [False for i in range(len(REG))]
    solvedHeap = [not i for i in initialisedHEAP2]
    solvedRegisters[0] = True
    
    # start with registers R1 -> Rx then heap M0 -> Mx
    dependencyStack = []

    combined = solvedRegisters + solvedHeap

    i = combined.index(False)
    while (False in solvedRegisters) or (False in solvedHeap):

        combined = solvedRegisters + solvedHeap

        #if i >= (len(REG) + len(HEAP)):
        #    i = combined.index(False)

        if i < len(REG):
            if solvedRegisters[i] == False:
            
                # this is a register

                initalRegName = f"R{i}"
                value = str(REG[i])

                if value == initalRegName:
                    # mark register as solved
                    solvedRegisters[i] = True
                    i = combined.index(False)
                    dependencyStack = []

                elif value.startswith(("R", "M")):
                    # depends on another register or heap
                    
                    # find if the original register is dependent on another register/heap location
                    dependent = False
                    for j in range(len(REG)):
                        if str(REG[j]) == initalRegName:
                            dependent = True
                            # set index to solve the dependency
                            i = j
                            # if this register is already in dependencyStack, crash
                            if initalRegName in dependencyStack:
                                raise Exception("bad dependency")
                            # add reg to dependencyStack
                            dependencyStack.append(initalRegName)
                            break
                    for j in range(len(HEAP)):
                        if str(HEAP[j]) == initalRegName:
                            dependent = True
                            # set index to solve the dependency
                            i = j + len(REG)
                            # if this register is already in dependencyStack, crash
                            if initalRegName in dependencyStack:
                                raise Exception("bad dependency")
                            # add reg to dependencyStack
                            dependencyStack.append(initalRegName)
                            break
                    
                    if not dependent:
                        # this reg can be successfully solved
                        
                        if value.startswith("R"):
                            resultInstructions.append(["MOV", initalRegName, value])
                            # mark register as solved
                            solvedRegisters[i] = True
                            i = combined.index(False)
                            dependencyStack = []
                        elif value.startswith("M"):
                            resultInstructions.append(["LOD", initalRegName, value])
                            # mark register as solved
                            solvedRegisters[i] = True
                            i = combined.index(False)
                            dependencyStack = []
                        else:
                            raise Exception("oppsie")

                else:
                    resultInstructions.append(["IMM", f"R{i}", value])
                    # mark register as solved
                    solvedRegisters[i] = True
                    i = combined.index(False)
                    dependencyStack = []
                    
            else:
                # already solved
                i = combined.index(False)

        else:
            if solvedHeap[i - len(REG)] == False:
            
                # this is a heap location

                initalHeapName = f"M{i - len(REG)}"
                value = str(HEAP[i - len(REG)])

                if value == initalHeapName:
                    # mark heap as solved
                    solvedHeap[i - len(REG)] = True
                    i = combined.index(False)
                    dependencyStack = []

                elif value.startswith(("R", "M")):
                    # depends on another register or heap
                    
                    # find if the original heap location is dependent on another register/heap location
                    dependent = False
                    for j in range(len(REG)):
                        if str(REG[j]) == initalHeapName:
                            dependent = True
                            # set index to solve the dependency
                            i = j
                            # if this heap location is already in dependencyStack, crash
                            if initalHeapName in dependencyStack:
                                raise Exception("bad dependency")
                            # add heap to dependencyStack
                            dependencyStack.append(initalHeapName)
                            break
                    for j in range(len(HEAP)):
                        if str(HEAP[j]) == initalHeapName:
                            dependent = True
                            # set index to solve the dependency
                            i = j + len(REG)
                            # if this heap location is already in dependencyStack, crash
                            if initalHeapName in dependencyStack:
                                raise Exception("bad dependency")
                            # add heap to dependencyStack
                            dependencyStack.append(initalHeapName)
                            break
                    
                    if not dependent:
                        # this heap location can be successfully solved
                        
                        if value.startswith("R"):
                            resultInstructions.append(["STR", initalHeapName, value])
                            # mark heap as solved
                            solvedHeap[i - len(REG)] = True
                            i = combined.index(False)
                            dependencyStack = []
                        elif value.startswith("M"):
                            resultInstructions.append(["CPY", initalHeapName, value])
                            # mark heap as solved
                            solvedHeap[i - len(REG)] = True
                            i = combined.index(False)
                            dependencyStack = []
                        else:
                            raise Exception("oppsie")

                else:
                    resultInstructions.append(["STR", f"M{i - len(REG)}", value])
                    # mark heap location as solved
                    solvedHeap[i - len(REG)] = True
                    i = combined.index(False)
                    dependencyStack = []
            else:
                # already solved
                i = combined.index(False)
    
    # old register and heap generating code (doesn't handle dependencies)
    """for index in range(len(REG)):
        if initialisedREG[index]:
            resultInstructions.append(["IMM", f"R{index}", str(REG[index])])
    for index in range(len(HEAP)):
        if initialisedHEAP[index]:
            resultInstructions.append(["STR", f"M{index}", str(HEAP[index])])"""

    if appendHLT:
        resultInstructions.append(["HLT"])

    # fix heapLocations in codeBlock
    for index, line in enumerate(codeBlock):
        if line[0] == "STR":
            if line[1].isnumeric():
                codeBlock[index][1] = f"M{int(line[1]) + M0}"

    # calculate new cost
    newCost = len(resultInstructions)
    for line in resultInstructions:
        if line[0] in ("LOD", "STR", "MLT", "DIV", "UMLT"):
            newCost += 1
        elif line[0] in ("LLOD", "LSTR", "CPY"):
            newCost += 2
        elif line[0] == "SDIV":
            newCost += 3

    if (newCost >= cycles) or (resultInstructions == codeBlock):
        raise Exception("Optimised code is worse than the initial codeblock")

    # convert R29 back into SP
    for index, line in enumerate(resultInstructions):
        for index2, token in enumerate(line):
            if token == "R29":
                resultInstructions[index][index2] = "SP"

    return resultInstructions
