# URCL-Optimiser-V2

A generic URCL code optimiser, that prioritises only OUT instructions.

#

#

# URCL Optimisation Rules

These optimisations can all be applied independently to URCL code.

To optimise a URCL program as much as possible, all rules should be applied repeatedly until the code cannot be improved by any of the rules.

## Code Cleaning

Optimsations focused on removing useless parts of the code and transforming it into easier to parse code.

#

### Remove Comments:

Delete all line and multi-line comments.

This rule may:
- Not delete any instructions
- Not delete any labels

Example:
```
/*
Multi-line comment
*/
ADD R1 R2 R3 // line comment
```
Optimises to:
```
ADD R1 R2 R3
```

#

### Unify Spaces:

Replaces all instances of multiple spaces, with single spaces and removes any spaces at the start of all lines.

This rule may:
- Not delete any instructions
- Not delete any labels

Example:
```
    IMM R1 5
ADD R1 R2    R3
```
Optimises to:
```
IMM R1 5
ADD R1 R2 R3
```

#

### Remove Empty Lines:

Delete empty lines.

This rule may:
- Not delete any instructions
- Not delete any labels

Example:
```
IMM R1 5

ADD R1 R2 R3
```
Optimises to:
```
IMM R1 5
ADD R1 R2 R3
```

#

### Define Macros:

Resolve and remove `@DEFINE` macros.

This will raise a warning if there are unused define macros.

This will raise an exception if there are macros other than define ones or if a define macro has more than 2 tokens associated with it.

This rule may:
- Delete @DEFINE macros
- Replace operands within instructions

Example:
```
@DEFINE hi R1
IMM hi 5
```
Optimises to:
```
IMM R1 5
```

#

### Convert Bases:

Convert all base 2 and base 16 numbers to base 10.

This rule may:
- Replace operands within instructions

Example:
```
IMM R1 0b101
```
Optimises to:
```
IMM R1 5
```

#

### Tokenise:

Splits the code into separate tokens using single spaces " ".

This rule only helps with parsing, it does not change the code in any meaningful way.

This rule may:
- Not delete any instructions
- Not delete any labels

#

### Fix BITS Header Syntax:

Remove the "==" from the BITS header if it exists.

Raises an exception if ">=" or "<=" is used, as this optimiser is only designed for fixed values for BITS.

Raises a warning if no BITS header is found. In this case it will assume `BITS 16`.

This rule may:
- Replace the BITS header

Example:
```
BITS == 8
```
Optimises to:
```
BITS 8
```

#

### Fix Negative Values:

Convert all negative immediate values (ignoring relative values) into positive values.

This rule may:
- Replace operands within instructions

Example:
```
BITS 8
IMM R1 -5
```
Optimises to:
```
BITS 8
IMM R1 251
```

#

### Convert Defined Immediates:

Replace defined immediates with the number that they represent.

This rule may:
- Replace operands within instructions

Example:
```
BITS 8
IMM R1 @MAX
```
Optimises to:
```
BITS 8
IMM R1 255
```

#

### Relatives to Labels:

Converts all relative values into unique labels.

This rule may:
- Not delete any instructions
- Replace operands within instructions
- Add new labels to the code

Example:
```
JMP ~+0
```
Optimises to:
```
.label
JMP .label
```

#

### Standardise Symbols

Replaces '#' with 'M' and '$' with 'R'. Capitalises all letters in the code except for labels, and any text in quotes or double quotes.

This rule may:
- Not change the code in any meaningful way

Example:
```
lod r1 #1
```
Optimises to:
```
LOD R1 M1
```

#

### Remove Unused Labels:

Removes any labels that are not referenced by any of the instructions.

This rule may:
- Not delete any instructions
- Delete labels

Example:
```
.label
NOP
```
Optimises to:
```
NOP
```

#

### Remove Multi-Labels:

Replaces multiple labels that point to the same instruction with one label. Replacing all instants of the removed labels with the label not deleted.

This rule may:
- Not delete any instructions
- Delete labels
- Replace operands within instructions

Example:
```
.label
.test
.hello
IMM R1 .test
IMM R2 .hello
```
Optimises to:
```
.label
IMM R1 .label
IMM R2 .label
```

#

### Move DW Values:

Moves all DW values within the code to the end of the code.

Labels that point to DW values are moved along with the DW values.

The sequential order of the DW values are preseved when moving them.

    WARNING - This will break code that contains labels that point to the end of DW values, as these will not be seen as labels that point to the DW values.

This rule may:
- Not delete any instructions
- Move DW values
- Move labels

Example:
```
.label
DW 6
IMM R1 9
```
Optimises to:
```
IMM R1 9
.label
DW 6
```

#

### Remove Unreachable Code:

Deletes unreachable sections of code. Sections of code are deemed unreachable if it does not start with a label that is referenced somewhere else in the program (self-reference doesn't count).

This rule may:
- Delete instructions
- Not delete labels

Example:
```
JMP .label
IMM R1 1
.label
```
Optimises to:
```
JMP .label
.label
```

#

### Reduce Registers:

Tries to reduce the minimum required number of registers to run a program by detecting and removing unused registers.

This rule may:
- Replace operands within instructions

Example:
```
MINREG 2
IMM R2 6
```
Optimises to:
```
MINREG 1
IMM R1 6
```

#

### Recalculate Headers:

Deletes the old header information and replaces it with the least expensive header information calculated by the optimiser.

This may add headers if the source code is missing them.

In cases where the headers cannot be calculated, the original version of that header will be used. Or if the original header does not exist, it will omit that header entirely.

This rule may:
- Delete instructions
- Not delete labels
- Replace headers values

Example:
```
BITS 8
MINREG 15
RUN RAM
ADD R1 R2 R3
```
Optimises to:
```
BITS 8
MINREG 3
RUN RAM
MINHEAP 0
MINSTACK 0
ADD R1 R2 R3
```

#

#

## Main Optimisations:

Optimsations focused on speeding up the runtime of the code by simplifying it.

#

### Remove R0:

Instructions that write to R0 do nothing so they are removed.

Instructions that read from R0, have the R0 replaced with the immediate value of 0.

This rule may:
- Delete instructions
- Replace operands within instructions

Example:
```
ADD R0 R2 R3
ADD R1 R2 R0
```
Optimises to:
```
ADD R1 R2 0
```

#

### Remove NOPs:

Deletes all NOP instructions.

This rule may:
- Delete instructions

Example:
```
NOP
NOP
```
Optimises to:
```

```

#

### Shortcut Branches:

Branches (or jumps) that branch to another JMP instruction will have their branch address updated to the location the second JMP goes to.

This rule may:
- Not delete any instructions
- Replace operands within instructions

Example:
```
BRZ .label R1
.label
JMP .label2
.label2
NOP
```
Optimises to:
```
BRZ .label2 R1
.label
JMP .label2
.label2
NOP
```

#

### Remove Pointless Branches:

Deletes branches (and jumps) that branch to the instruction immediately after that instruction.

This rule may:
- Delete instructions
- Not delete labels

Example:
```
BRZ .label R1
.label
NOP
```
Optimises to:
```
.label
NOP
```

#

### JMP to Subroutine:

Optimise JMP instructions that jump to a CAL, RET or HLT instruction.

This rule may:
- Replace instructions with other instructions
- Not delete labels

Example:
```
JMP .label
.label
RET
```
Optimises to:
```
RET
.label
RET
```

Example:
```
JMP .label
.label
CAL .label
```
Optimises to:
```
CAL .label
.label
CAL .label
```

#

### Immediate Folding:
Calculates the results of single instructions that only read immediate values.

This rule may:
- Delete instructions
- Replace instructions with other instructions

Example:
```
.label
ADD R1 4 5
BRZ .label R1
```
Optimises to:
```
.label
IMM R1 9
JMP .label
```

#

### Immediate Propagation:

Propagates immediate values from IMM instructions forwards to future instructions.

This rule may:
- Not delete any instructions
- Replace operands within instructions

Example:
```
IMM R1 5
ADD R1 R1 R2
```
Optimises to:
```
IMM R1 5
ADD R1 5 R2
```

#

### Write Before Read:

Optimise code that overwrites a register twice without reading the first value.

This rule may:
- Delete instructions
- Not delete labels

Example:
```
IMM R1 5
ADD R1 R2 R3
```
Optimises to:
```
ADD R1 R2 R3
```

#

### Detect OUT Instructions:

If the code contains no OUT instructions, then delete all code as the code is deemed to do nothing.

This rule may:
- Delete all code

Example:
```
ADD R1 R2 R3
```
Optimises to:
```

```

#

### Inline Branches:

Sections of code that are referred to only once in the code by the address of a single branch instruction, and are otherwise inaccessable, and end with a JMP, RET or HLT instruction - are inlined.

Self-references do not count.

Sections of code must end in a JMP, RET or HLT instruction (unconditional branch or halt), otherwise the section cannot be moved.

This rule may:
- Move instructions
- Delete instructions
- Not delete labels

Example:
```
JMP .label
.halt
HLT
.label
NOP
JMP .halt
```
Optimises to:
```
.label
NOP
JMP .halt
.halt
HLT
```

#

### Inverse Branches

Optimise branch instructions that branch 2 instructions ahead followed by a JMP instruction, by inverting the branch condition.

This rule may:
- Replace instructions with other instructions
- Delete instructions
- Not delete labels

Example:
```
BRZ .label R1
JMP .test
.label
HLT
.test
HLT
```
Optimises to:
```
BNZ .test R1
.label
HLT
.test
HLT
```

#

### Pointless Writes:

Instructions that write to registers that are never read anywhere in the entire program are removed.

This rule may:
- Delete instructions

Example:
```
IMM R1 5
HLT
```
Optimises to:
```
HLT
```

#

### Duplicate Loads:

Loading a value using an immediate address more than once without overwriting the original value is optimised by removing the unneeded LOD instructions.

This rule may:
- Delete instructions

Example:
```
LOD R1 M1
ADD R2 R1 5
LOD R1 M1
```
Optimises to:
```
LOD R1 M1
ADD R2 R1 5
```

#

### Propagate MOV:

Propagate MOV instruction values where the source register has not yet been overwritten.

This rule may:
- Not delete any instructions
- Replace operands within instructions

Example:
```
MOV R2 R4
ADD R1 R2 R3
```
Optimises to:
```
MOV R2 R4
ADD R1 R4 R3
```

#

#

## Single Instruction Optimisations

These are optimisations that are applied to individual instructions, ignoring the rest of the program.

#

### ADD to LSH:

Convert ADD to LSH if adding something to itself.

Example:
```
ADD R1 R2 R2
```
Optimises to:
```
LSH R1 R2
```

#

### ADD to MOV:

Convert ADD to MOV if adding something to zero.

Example:
```
ADD R1 R2 0
```
Optimises to:
```
MOV R1 R2
```

#

### BGE to JMP:

Convert BGE to JMP if the third operand is 0, or the second operand is @MAX.

Example:
```
BGE .label R1 0
BGE .label @MAX R2
```
Optimises to:
```
JMP .label
JMP .label
```

#

### BGE to BNZ:

Convert BGE to BNZ if the third operand is 1.

Example:
```
BGE .label R1 1
```
Optimises to:
```
BNZ .label R1
```

#

### BGE to BRZ:

Convert BGE to BRZ if the second operand is 0.

Example:
```
BGE .label 0 R1
```
Optimises to:
```
BRZ .label R1
```

#

### NOR to NOT:

Convert NOR to NOT if the second or third operand is 0, or if the second and third operands are equal.

Example:
```
NOR R1 R2 0
NOR R1 R1 R1
```
Optimises to:
```
NOT R1 R2
NOT R1 R1
```

#

### NOR to IMM Zero:

Convert NOR to IMM if the second or third operands are @MAX.

Example:
```
BITS 8
NOR R1 R2 255
```
Optimises to:
```
BITS 8
IMM R1 0
```

#

### MOV to IMM:

Convert MOV to IMM if the second operand is an immediate value or label.

Example:
```
MOV R1 5
```
Optimises to:
```
IMM R1 5
```

#

#

## Instruction Pair Optimisations

Optimisations that are applied to pairs of sequential instructions.

A lot of these rules aim to decouple chains of instructions that operate on the same register. This itself does not make the code shorter or faster, but other optimisation rules may be able to take advantage of it.

#

### SETBranch:

Optimises a SET instruction followed by a conditional branch instruction based solely on the output of the SET instruction.

The code between the SET and branch must not contain labels or instructions that read from or write to the register SET writes to.

The code between must occur before the branch instruction after applying this optimisation.

Example:
```
SETGE R1 R2 R3
IMM R4 5
BNZ .label R1
```
Optimises to:
```
SETGE R1 R2 R3
IMM R4 5
BGE .label R2 R3
```

#

### LODSTR:

Optimises LOD followed by a STR instruction where the memory location is the same and the register is the same.

The code between must not contain any labels or any instructions that write to the shared register.

If the shared memory location is a register, the instructions between must not write to that register.

Example:
```
LOD R1 M0
IMM R2 5
STR M0 R1
```
Optimises to:
```
LOD R1 M0
IMM R2 5
```

#

### STRLOD:

Optimises STR followed by a LOD instruction where the memory location is the same and the register is the same.

The code between must not contain any labels or any instructions that write to the shared memory location.

If the shared memory location is a register, the instructions between must not write to that register.

Example:
```
STR M0 R1
IMM R2 5
LOD R1 M0
```
Optimises to:
```
STR M0 R1
IMM R2 5
```

#

### ADDADD:

Optimises ADD followed by an ADD instruction where the register written to by the first ADD is read and written to by the second one.

The first and second ADD instructions must both contain immediate values (specifically raw numbers, not labels or heap locations).

The code between must not contain any labels, or any instructions that write to the register written to by the first ADD, or instuctions that write to the register read by the first ADD.

Example:
```
ADD R1 R2 100
MOV R3 R1
ADD R1 R1 200
```
Optimises to:
```
ADD R1 R2 100
MOV R3 R1
ADD R1 R2 300
```

#

### SUBSUB:

Optimises SUB followed by a SUB instruction where both instructions write to the same register and they both contain one immediate value (specifically raw numbers, not labels or heap locations).

The registers read and written to by the first SUB must not be written to by the code between. The code between must not contain any labels.

Example:
```
SUB R1 R2 100
MOV R3 R1
SUB R1 R1 200
```
Optimises to:
```
SUB R1 R2 100
MOV R3 R1
SUB R1 R2 300
```

#

### INCINC:

Optimises INC followed by a INC instruction where both instructions write to the same register.

The registers read and written to by the first INC must not be written to by the code between. The code between must not contain any labels.

Example:
```
INC R1 R2
MOV R3 R1
INC R1 R1
```
Optimises to:
```
INC R1 R2
MOV R3 R1
ADD R1 R2 2
```

#

### DECDEC:

Optimises DEC followed by a DEC instruction where both instructions write to the same register.

The registers read and written to by the first DEC must not be written to by the code between. The code between must not contain any labels.

Example:
```
DEC R1 R2
MOV R3 R1
DEC R1 R1
```
Optimises to:
```
DEC R1 R2
MOV R3 R1
SUB R1 R2 2
```

#

### ADDSUB:

Optimises ADD followed by a SUB instruction where both instructions write to the same register and they both contain one immediate value (specifically raw numbers, not labels or heap locations). 

The registers read and written to by the first ADD must not be written to by the code between. The code between must not contain any labels.

Example:
```
ADD R1 R2 5
MOV R3 R1
SUB R1 10 R1
```
Optimises to:
```
ADD R1 R2 5
MOV R3 R1
SUB R1 5 R2
```

#

### ADDINC:

Optimises ADD followed by a INC instruction where both instructions write to the same register and the ADD contains one immediate value (specifically raw numbers, not labels or heap locations). 

The registers read and written to by the first ADD must not be written to by the code between. The code between must not contain any labels.

Example:
```
ADD R1 R2 5
MOV R3 R1
INC R1 R1
```
Optimises to:
```
ADD R1 R2 5
MOV R3 R1
ADD R1 R2 6
```

#

### ADDDEC:

Optimises ADD followed by a DEC instruction where both instructions write to the same register and the ADD contains one immediate value (specifically raw numbers, not labels or heap locations). 

The registers read and written to by the first ADD must not be written to by the code between. The code between must not contain any labels.

Example:
```
ADD R1 R2 5
MOV R3 R1
DEC R1 R1
```
Optimises to:
```
ADD R1 R2 5
MOV R3 R1
ADD R1 R2 5
```

#

### SUBINC:

Optimises SUB followed by a INC instruction where both instructions write to the same register and the SUB contains one immediate value (specifically raw numbers, not labels or heap locations). 

The registers read and written to by the first SUB must not be written to by the code between. The code between must not contain any labels.

Example:
```
SUB R1 R2 5
MOV R3 R1
INC R1 R1
```
Optimises to:
```
SUB R1 R2 5
MOV R3 R1
SUB R1 R2 4
```

### SUBDEC:

Optimises SUB followed by a DEC instruction where both instructions write to the same register and the SUB contains one immediate value (specifically raw numbers, not labels or heap locations). 

The registers read and written to by the first SUB must not be written to by the code between. The code between must not contain any labels.

Example:
```
SUB R1 R2 5
MOV R3 R1
DEC R1 R1
```
Optimises to:
```
SUB R1 R2 5
MOV R3 R1
SUB R1 R2 6
```

#

### INCDEC:

Optimises INC followed by a DEC instruction where both instructions write to the same register.

The registers read and written to by the first INC must not be written to by the code between. The code between must not contain any labels.

Example:
```
INC R1 R2
MOV R3 R1
DEC R1 R1
```
Optimises to:
```
INC R1 R2
MOV R3 R1
MOV R1 R2
```

#

### SUBADD:

Optimises SUB followed by a ADD instruction where both instructions write to the same register and they both contain one immediate value (specifically raw numbers, not labels or heap locations).

The registers read and written to by the first SUB must not be written to by the code between. The code between must not contain any labels.

Example:
```
SUB R1 R2 300
MOV R3 R1
ADD R1 R1 100
```
Optimises to:
```
SUB R1 R2 300
MOV R3 R1
SUB R1 R2 200
```

#

### INCADD:

Optimises INC followed by a ADD instruction where both instructions write to the same register.

The registers read and written to by the first INC must not be written to by the code between. The code between must not contain any labels.

Example:
```
INC R1 R2
MOV R3 R1
ADD R1 R1 5
```
Optimises to:
```
INC R1 R2
MOV R3 R1
ADD R1 R2 6
```

#

### DECADD:

Optimises DEC followed by a ADD instruction where both instructions write to the same register.

The registers read and written to by the first DEC must not be written to by the code between. The code between must not contain any labels.

Example:
```
DEC R1 R2
MOV R3 R1
ADD R1 R1 5
```
Optimises to:
```
DEC R1 R2
MOV R3 R1
ADD R1 R2 4
```

#

### INCSUB:

Optimises INC followed by a SUB instruction where both instructions write to the same register.

The registers read and written to by the first INC must not be written to by the code between. The code between must not contain any labels.

Example:
```
INC R1 R2
MOV R3 R1
SUB R1 R1 5
```
Optimises to:
```
INC R1 R2
MOV R3 R1
SUB R1 R2 4
```

#

### DECSUB:

Optimises DEC followed by a SUB instruction where both instructions write to the same register.

The registers read and written to by the first DEC must not be written to by the code between. The code between must not contain any labels.

Example:
```
DEC R1 R2
MOV R3 R1
SUB R1 R1 5
```
Optimises to:
```
DEC R1 R2
MOV R3 R1
SUB R1 R2 6
```

#

### DECINC:

Optimises DEC followed by a INC instruction where both instructions write to the same register.

The registers read and written to by the first DEC must not be written to by the code between. The code between must not contain any labels.

Example:
```
DEC R1 R2
MOV R3 R1
INC R1 R1
```
Optimises to:
```
DEC R1 R2
MOV R3 R1
MOV R1 R2
```

#

### MLTMLT:

Optimises MLT followed by an MLT instruction where the register written to by the first MLT is read and written to by the second one.

The first and second MLT instructions must both contain immediate values (specifically raw numbers, not labels or heap locations).

The code between must not contain any labels, or any instructions that read or write to the register written to by the first MLT.

Example:
```
MLT R1 R2 10
MOV R3 R1
MLT R1 R1 20
```
Optimises to:
```
MLT R1 R2 10
MOV R3 R1
MLT R1 R2 200
```

#

### DIVDIV:
### LSHLSH:
### RSHRSH:
### SRSSRS:
### BSLBSL:
### BSRBSR:
### BSSBSS:
### LSHBSL:
### BSLLSH:
### RSHBSR:
### BSRRSH:
### SRSBSS:
### BSSSRS:
### RSHSRS:
### RSHBSS:
### LSHRSH:
### RSHLSH:
### LSHBSR:
### BSRLSH:
### RSHBSL:
### BSLRSH:
### BSLBSR:
### BSRBSL:
### ANDAND:
### XORXOR:
### PSHPOP (no code between):
#



