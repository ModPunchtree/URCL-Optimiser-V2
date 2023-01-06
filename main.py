# main file for repl.it 

import discord
import os
from random import randint
from keep_alive import keep_alive
import asyncio
from URCLOptimiserV2.optimiser_main import optimiseURCL

from SYL_Compiler.tokeniser import tokenise
from SYL_Compiler.preprocess import preprocess
from SYL_Compiler.distinguisher import distinguisher
from SYL_Compiler.shuntingYard import shuntingYard
from SYL_Compiler.precompileOptimiser import precompileOptimiser
from SYL_Compiler.generateURCL import generateURCL
from SYL_Compiler.memoryMap import memoryMap

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Username: " + str(client.user))


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    elif message.content.startswith("$lol"):
        if str(message.author) == "Mod Punchtree#5817":
            await message.channel.send(":regional_indicator_l::regional_indicator_o::regional_indicator_l:")
        elif randint(1, 20) == 1:
            await message.channel.send("```\nFatal - Token too big:\nyoMamma\n      ^\n```")
        else:
            await message.channel.send(":regional_indicator_l::regional_indicator_o::regional_indicator_l:")

    elif message.content.startswith("$help") and str(message.channel) not in ("syl-compiler", ""):
        await message.channel.send(":woman_shrugging:")
        return

    elif str(message.channel) not in ("syl-compiler", ""):
        return

    elif message.content.startswith("$help"):
        await message.channel.send("""To optimise URCL code do:\n$optimise```c\n// URCL code goes here```To "LOL" type:\n$lol""")
        return

    elif message.content.startswith("$optimise"):
        await message.channel.send("Optimising...")
        try:
            code = message.content[9: ]
            if code.find("```\n") == -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[code.index("```\n") + 4: ]
            if code.find("```") == -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[: code.index("```")]
            
            code, optimisationCount = optimiseURCL(code, 300)
            
            result = ""
            for line in code:
                result += " ".join(line)
                result += "\n"

            if result[-1] == "\n":
                result = result[: -1]
            
        except Exception as x:
            await message.channel.send(f"ERROR: \n{x}")
            return
        f = open("output.txt", "w")
        f.write(result)
        f.close()
        await message.channel.send(f"Success!\nNumber of optimisations applied: {optimisationCount}")
        if len(result) < 500:
            await message.channel.send(f"```\n{result}```")
        else:
            await message.channel.send(file=discord.File("output.txt"))
        return

    elif message.content.startswith(("$SYLcompile -o", "$SYLcompile -O", "$SYLcompile-o", "$SYLcompile-O")):
        # no optimisations
        await message.channel.send("Compiling...")
        try:
            code = message.content[9: ]
            if code.find("```\n") == -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[code.index("```\n") + 4: ]
            if code.find("```") == -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[: code.index("```")]
            
            BITS = 16
            MINREG = 25
            
            code = tokenise(code)
            
            code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = preprocess(code)
            
            code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = distinguisher(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = shuntingYard(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            code = precompileOptimiser(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            URCL, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths = generateURCL(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            URCL = memoryMap(URCL, funcNames, funcMapNames, funcMapLocations, BITS, MINREG, functionTypes)
            
            result = []
            for line in URCL:
                text = " ".join(line)
                result.append(text)
            result = "\n".join(result)
            
        except Exception as x:
            await message.channel.send(f"ERROR: \n{x}")
            return
        f = open("output.txt", "w")
        f.write(result)
        f.close()
        await message.channel.send(f"Success!\nNumber of optimisations applied: 0")
        if len(result) < 500:
            await message.channel.send(f"```\n{result}```")
        else:
            await message.channel.send(file=discord.File("output.txt"))
        return

    elif message.content.startswith("$SYLcompile"):
        await message.channel.send("Compiling...")
        try:
            code = message.content[9: ]
            if code.find("```\n") == -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[code.index("```\n") + 4: ]
            if code.find("```") == -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[: code.index("```")]
            
            BITS = 16
            MINREG = 25
            
            code = tokenise(code)
            
            code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = preprocess(code)
            
            code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = distinguisher(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths = shuntingYard(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            code = precompileOptimiser(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            URCL, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths = generateURCL(code, varNames, funcNames, arrNames, funcMapNames, funcMapLocations, BITS, MINREG, variableTypes, functionTypes, arrayTypes, arrayLengths)
            
            URCL = memoryMap(URCL, funcNames, funcMapNames, funcMapLocations, BITS, MINREG, functionTypes)
            
            code2 = []
            for line in URCL:
                text = " ".join(line)
                code2.append(text)
            code2 = "\n".join(code2)
            
            # code is now ready for optimisation
            
            code2, optimisationCount = optimiseURCL(code2, 500, 0, 20)
            
            result = ""
            for line in code2:
                result += " ".join(line)
                result += "\n"

            if result[-1] == "\n":
                result = result[: -1]
            
        except Exception as x:
            await message.channel.send(f"ERROR: \n{x}")
            return
        f = open("output.txt", "w")
        f.write(result)
        f.close()
        await message.channel.send(f"Success!\nNumber of optimisations applied: {optimisationCount}")
        if len(result) < 500:
            await message.channel.send(f"```\n{result}```")
        else:
            await message.channel.send(file=discord.File("output.txt"))
        return

    else:
        return

keep_alive()
client.run(os.getenv("TOKEN"))
