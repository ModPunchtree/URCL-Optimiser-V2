
from SYL_Compiler.tokeniser import tokenise
from SYL_Compiler.preprocess import preprocess
from SYL_Compiler.distinguisher import distinguisher
from SYL_Compiler.shuntingYard import shuntingYard
from SYL_Compiler.precompileOptimiser import precompileOptimiser
from SYL_Compiler.generateURCL import generateURCL
from SYL_Compiler.memoryMap import memoryMap
from copy import deepcopy

f = open("test.syl")
code = f.read()
f.close()

BITS = 16
MINREG = 25

code = tokenise(code)

code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = preprocess(code)

code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = distinguisher(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths)

# make code more readable
code2 = " ".join(code).replace(" ,", ",").replace(" ;", ";").replace("; ", ";").replace("( ", "(").replace(" )", ")").replace("{ ", "{").replace(" }", "}").replace(" [", "[").replace("[ ", "[").replace(" ]", "]").replace("} ", "}").replace(";", ";\n").replace("{", "{\n").replace("}", "}\n")

code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = shuntingYard(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths)

code = precompileOptimiser(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths)

# make code more readable
code3 = " ".join(code).replace("; ", ";\n").replace("{ ", "{\n").replace("} ", "}\n")

URCL, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths = generateURCL(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths)

URCL = memoryMap(URCL, funcNames, funcMapNames, funcMapLocations, BITS, MINREG, functionTypes)

# make urcl code more readable
code4 = []
for line in URCL:
    text = " ".join(line)
    code4.append(text)
code4 = "\n".join(code4)

# code is now ready for optimisations

print(f"\n#####################  Unoptimised URCL:  #####################\n\n{code4}\n\n#####################  Reverse Polish:  #####################\n\n{code3}\n\n#####################  Original SYL Code:  #####################\n\n{code2}\n\n#####################  Info:  #####################\n\nvarNames: {varNames}\nvariableTypes: {variableTypes}\nfuncNames: {funcNames}\nfunctionTypes: {functionTypes}\narrNames: {arrNames}\narrayTypes: {arrayTypes}\nfuncMapNames: {funcMapNames}\nfuncMapLocations: {funcMapLocations}\n")
#print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n{code3}\n\n\n\n\n\n\n\n\n")




