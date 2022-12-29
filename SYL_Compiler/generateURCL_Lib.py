
def binaryOperator(operator: str, tempVarReg: str, leftInput: str, leftType: str, rightInput: str, rightType: str):
    
    void = False
    answer = 0
    
    # try to make void types work
    if (rightType == "void") and (leftType == "void"):
        void = True
        rightType = "uint"
        leftType = "uint"
    elif leftType == "void":
        leftType = rightType
    elif rightType == "void":
         rightType = leftType
    
    types = (leftType, rightType)
    
    match operator:
        case "%":
            match types:
                case ("uint", "uint"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["MOD", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "/":
            match types:
                case ("int", "int"):
                    answer = [["SDIV", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["SDIV", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["SDIV", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["SDIV", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["DIV", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "BINARY*":
            match types:
                case ("int", "int"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["MLT", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "BINARY-":
            match types:
                case ("int", "int"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char"
                case ("int*", "int*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int*"
                case ("int*", "constint*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int*"
                case ("constint*", "int*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int*"
                case ("constint*", "constint*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "int*"
                case ("uint*", "uint*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint*"
                case ("uint*", "constuint*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint*"
                case ("constuint*", "uint*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint*"
                case ("constuint*", "constuint*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "uint*"
                case ("char*", "char*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char*"
                case ("char*", "constchar*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char*"
                case ("constchar*", "char*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char*"
                case ("constchar*", "constchar*"):
                    answer = [["SUB", tempVarReg, leftInput, rightInput]], "char*"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "BINARY+":
            match types:
                case ("int", "int"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char"
                case ("int*", "int*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int*"
                case ("int*", "constint*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int*"
                case ("constint*", "int*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int*"
                case ("constint*", "constint*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "int*"
                case ("uint*", "uint*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint*"
                case ("uint*", "constuint*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint*"
                case ("constuint*", "uint*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint*"
                case ("constuint*", "constuint*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "uint*"
                case ("char*", "char*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char*"
                case ("char*", "constchar*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char*"
                case ("constchar*", "char*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char*"
                case ("constchar*", "constchar*"):
                    answer = [["ADD", tempVarReg, leftInput, rightInput]], "char*"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case ">>":
            match types:
                case ("int", "int"):
                    answer = [["BSS", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["BSS", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["BSS", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["BSS", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["BSR", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "<<":
            match types:
                case ("int", "int"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["BSL", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case ">=":
            match types:
                case ("int", "int"):
                    answer = [["SSETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int", "constint"):
                    answer = [["SSETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "int"):
                    answer = [["SSETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "constint"):
                    answer = [["SSETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "uint"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "char"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "constchar"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "char"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "bool"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "int*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "constint*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "int*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "constint*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "uint*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "constuint*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "uint*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "constuint*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "char*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "constchar*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "char*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "constchar*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "bool*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "constbool*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "bool*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "constbool*"):
                    answer = [["SETGE", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case ">":
            match types:
                case ("int", "int"):
                    answer = [["SSETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("int", "constint"):
                    answer = [["SSETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "int"):
                    answer = [["SSETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "constint"):
                    answer = [["SSETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "uint"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "char"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "constchar"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "char"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "bool"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "int*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "constint*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "int*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "constint*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "uint*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "constuint*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "uint*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "constuint*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "char*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "constchar*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "char*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "constchar*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "bool*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "constbool*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "bool*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "constbool*"):
                    answer = [["SETG", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "<=":
            match types:
                case ("int", "int"):
                    answer = [["SSETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int", "constint"):
                    answer = [["SSETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "int"):
                    answer = [["SSETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "constint"):
                    answer = [["SSETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "uint"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "char"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "constchar"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "char"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "bool"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "int*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "constint*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "int*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "constint*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "uint*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "constuint*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "uint*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "constuint*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "char*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "constchar*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "char*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "constchar*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "bool*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "constbool*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "bool*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "constbool*"):
                    answer = [["SETLE", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "<":
            match types:
                case ("int", "int"):
                    answer = [["SSETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("int", "constint"):
                    answer = [["SSETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "int"):
                    answer = [["SSETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "constint"):
                    answer = [["SSETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "uint"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "char"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "constchar"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "char"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "bool"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "int*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "constint*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "int*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "constint*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "uint*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "constuint*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "uint*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "constuint*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "char*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "constchar*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "char*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "constchar*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "bool*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "constbool*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "bool*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "constbool*"):
                    answer = [["SETL", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "!=":
            match types:
                case ("int", "int"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int", "constint"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "int"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "constint"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "uint"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "char"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "constchar"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "char"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "bool"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "int*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "constint*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "int*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "constint*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "uint*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "constuint*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "uint*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "constuint*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "char*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "constchar*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "char*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "constchar*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "bool*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "constbool*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "bool*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "constbool*"):
                    answer = [["SETNE", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "==":
            match types:
                case ("int", "int"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int", "constint"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "int"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint", "constint"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "uint"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "char"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char", "constchar"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "char"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "bool"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "int*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("int*", "constint*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "int*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constint*", "constint*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "uint*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("uint*", "constuint*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "uint*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constuint*", "constuint*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "char*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("char*", "constchar*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "char*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constchar*", "constchar*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "bool*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool*", "constbool*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "bool*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool*", "constbool*"):
                    answer = [["SETE", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "BINARY&":
            match types:
                case ("int", "int"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "^":
            match types:
                case ("int", "int"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["XOR", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "|":
            match types:
                case ("int", "int"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "int"
                case ("int", "constint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "int"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "int"
                case ("constint", "constint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "int"
                case ("uint", "uint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "uint"
                case ("uint", "constuint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "uint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "uint"
                case ("constuint", "constuint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "uint"
                case ("char", "char"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "char"
                case ("char", "constchar"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "char"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "char"
                case ("constchar", "constchar"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "char"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "&&":
            match types:
                case ("int", "int"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("int", "constint"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constint", "int"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constint", "constint"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("uint", "uint"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("uint", "constuint"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constuint", "uint"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constuint", "constuint"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("char", "char"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("char", "constchar"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constchar", "char"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constchar", "constchar"):
                    answer = [["SETG", tempVarReg, leftInput, 0], ["AND", tempVarReg, rightInput, tempVarReg], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("bool", "bool"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["AND", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case "||":
            match types:
                case ("int", "int"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("int", "constint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constint", "int"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constint", "constint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("uint", "uint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("uint", "constuint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constuint", "uint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constuint", "constuint"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("char", "char"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("char", "constchar"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constchar", "char"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("constchar", "constchar"):
                    answer = [["OR", tempVarReg, leftInput, rightInput], ["SETG", tempVarReg, tempVarReg, 0]], "bool"
                case ("bool", "bool"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "bool"
                case ("bool", "constbool"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "bool"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "bool"
                case ("constbool", "constbool"):
                    answer = [["OR", tempVarReg, leftInput, rightInput]], "bool"
                case _:
                    raise Exception(f"Invalid operator types for: {operator}\nFound: {leftType} and {rightType}")
        case _:
            raise Exception(f"Unrecognised binary operator: {operator}")

    if void:
        if operator in (">=", ">", "<=", "<", "!=", "==", "&&", "||"):
            answer[1] = "bool"
        else:
            answer[1] = "void"

    return answer

def unaryOperator(operator: str, tempVarReg: str, singleInput: str, singleType: str, arrayLength = -1):
    
    void = False
    answer = 0
    
    # try to make void types work
    if singleType == "void":
        void = True
        singleType = "uint"########### might not be valid
    
    match operator:
        case "TYPECASTint":
            answer = [["MOV", tempVarReg, singleInput]], "int"
        case "TYPECASTuint":
            answer = [["MOV", tempVarReg, singleInput]], "uint"
        case "TYPECASTchar":
            answer = [["MOV", tempVarReg, singleInput]], "char"
        case "TYPECASTint*":
            answer = [["MOV", tempVarReg, singleInput]], "int*"
        case "TYPECASTuint*":
            answer = [["MOV", tempVarReg, singleInput]], "uint*"
        case "TYPECASTchar*":
            answer = [["MOV", tempVarReg, singleInput]], "char*"
        case "TYPECASTvoid":
            answer = [["MOV", tempVarReg, singleInput]], "void"
        case "TYPECASTbool":
            answer = [["MOV", tempVarReg, singleInput]], "bool"
        case "TYPECASTbool*":
            answer = [["MOV", tempVarReg, singleInput]], "bool*"
        case "TYPECASTconstint":
            answer = [["MOV", tempVarReg, singleInput]], "constint"
        case "TYPECASTconstuint":
            answer = [["MOV", tempVarReg, singleInput]], "constuint"
        case "TYPECASTconstchar":
            answer = [["MOV", tempVarReg, singleInput]], "constchar"
        case "TYPECASTconstint*":
            answer = [["MOV", tempVarReg, singleInput]], "constint*"
        case "TYPECASTconstuint*":
            answer = [["MOV", tempVarReg, singleInput]], "constuint*"
        case "TYPECASTconstchar*":
            answer = [["MOV", tempVarReg, singleInput]], "constchar*"
        case "TYPECASTconstvoid":
            answer = [["MOV", tempVarReg, singleInput]], "constvoid"
        case "TYPECASTconstbool":
            answer = [["MOV", tempVarReg, singleInput]], "constbool"
        case "TYPECASTconstbool*":
            answer = [["MOV", tempVarReg, singleInput]], "constbool*"
        case "sizeof":
            if arrayLength != -1:
                answer = [["IMM", tempVarReg, str(arrayLength)]], "uint"
            else:
                answer = [["IMM", tempVarReg, "1"]], "uint"
        case "UNARY*":
            match singleType:
                case "int*":
                    answer = [["LOD", tempVarReg, singleInput]], "int"
                case "uint*":
                    answer = [["LOD", tempVarReg, singleInput]], "uint"
                case "char*":
                    answer = [["LOD", tempVarReg, singleInput]], "char"
                case "bool*":
                    answer = [["LOD", tempVarReg, singleInput]], "bool"
                case "uint":
                    if void:
                        answer = [["LOD", tempVarReg, singleInput]], "void"
                    else:
                        raise Exception(f"Invalid operator type for: {operator}\nFound: {singleType}")
                case _:
                    raise Exception(f"Invalid operator type for: {operator}\nFound: {singleType}")
        case "UNARY+":
            answer = [["MOV", tempVarReg, singleInput]], singleType
        case "UNARY-":
            if singleType.find("bool") != -1:
                raise Exception(f"Invalid operator type for: {operator}\nFound: {singleType}")
            answer = [["NEG", tempVarReg, singleInput]], singleType
        case "~":
            if singleType.find("bool") != -1:
                raise Exception(f"Invalid operator type for: {operator}\nFound: {singleType}")
            answer = [["NOT", tempVarReg, singleInput]], singleType
        case "!":
            if singleType.find("bool") != -1:
                answer = [["NOT", tempVarReg, singleInput]], "bool"
            else:
                answer = [["SETL", tempVarReg, singleInput, "1"]], "bool"
        case _:
            raise Exception(f"Unrecognised binary operator: {operator}")

    # fix return type
    if void:
        if operator in (""):
            answer[1] = "bool"
        else:
            answer[1] = "void"

    return answer
