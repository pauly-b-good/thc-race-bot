import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

# loads discord bot token from the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

prefix = "/"
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(help="From a user given number or 10 (whichever is lower), a countdown begins and goes to 1 then GO! one second at a time.")
async def countdown(ctx, arg="10"):
    print("Countdown: executing")
    start_countdown_from = 10
    try:
        if arg.isdigit():
            start_countdown_from = int(arg) if int(arg) <= 10 else int(arg)
        for i in range(start_countdown_from, 0, -1):
            await ctx.send(f"{i}...")
            await asyncio.sleep(1)
        await ctx.send("GOOOOOOOOOOOOO!")
    except ValueError as v:
        print("An error occurred: {v}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("Countdown: completed")

@bot.command()
async def about(ctx):
    print("About: executing")
    try:
        await ctx.send("In the near future, this command is going to give information about the bot and its developers.")
    except Exception as e:
        print(f"An erro occurred: {e}")
    print("About: completed")

# @bot.command()
# async def help(ctx):
#     print("Help: executing")
#     try:
#         await ctx.send("In the near future, this command is going give a list of all available commands and descriptions for each")
#     except Exception as e:
#         print(f"An erro occurred: {e}")
#     print("Help: completed")




bot.run(DISCORD_TOKEN)
