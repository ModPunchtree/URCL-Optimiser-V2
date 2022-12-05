# main file for repl.it 

import discord
import os
from random import randint
from keep_alive import keep_alive
import asyncio
from URCLOptimiserV2.optimiser_main import optimiseURCL

client = discord.Client(intents=discord.Intents.default())


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

    elif message.content.startswith("$help") and str(message.channel) != "urcl-bot":
        await message.channel.send(":woman_shrugging:")
        return

    elif str(message.channel) != "urcl-optimiser":
        return

    elif message.content.startswith("$help"):
        await message.channel.send("""```c\nTo optimise URCL code do:\n$optimise```\n// URCL code goes here```To "LOL" do:\n$lol\n```""")
        return

    elif message.content.startswith("$optimise"):
        await message.channel.send("Compiling...")
        try:
            code = message.content[9: ]
            if code.find("```\n") != -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[code.index("```\n") + 4: ]
            if code.find("```") != -1:
                raise Exception("FATAL - Code block not specified (missing triple backticks: `)")
            code = code[: code.index("```")]
            
            code, optimisationCount = optimiseURCL(code)
            
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
        await message.channel.send(file=discord.File("output.txt"))
        return

    else:
        return

keep_alive()
client.run(os.getenv("TOKEN"))
