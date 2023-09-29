import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import time
import multiprocessing
from datetime import datetime
from colorama import Fore

# loads environment variables from the .env file
load_dotenv()
# DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
SETUP_INSTRUCTIONS_URL = os.getenv("SETUP_INSTRUCTIONS_URL")


print(Fore.GREEN + "THP-Race-Bot Script Started!")


# Discord Bot Permissions
prefix = "/"
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} at {datetime.now()}")


# /serverUrl Command
@bot.command(help = "Provides you with the THP Assetto Corsa Race Server URL.")
async def serverUrl(ctx):
    print(f"ServerUrl: executing at {datetime.now()}")
    try:
        await ctx.send(f"The THP Assetto Corsa server url is: {SERVER_URL}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print(f"ServerUrl: completed at {datetime.now()}")


# /assettoCorsaSetupInstructions
@bot.command(help = "Provides you with the Assetto Corsa setup instructions URL")
async def assettoCorsaSetupInstructions(ctx):
    print(f"AssettoCorsaSetupInstructions: executing at {datetime.now()}")
    try:
        await ctx.send(f"The THP Assetto Corsa setup instructions URL is: {SETUP_INSTRUCTIONS_URL}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print(f"AssettoCorsaSetupInstructions: completed at {datetime.now()}")


# /countdown [int] Command
@bot.command(help="From a user given number or 10 (whichever is lower), a countdown begins and goes to 1 then GO! one second at a time.")
async def countdown(ctx, arg="10"):
    print(f"Countdown: executing at {datetime.now()}")
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
    print(f"Countdown: completed at {datetime.now()}")


# /about command
@bot.command()
async def about(ctx):
    print(f"About: executing at {datetime.now()}")
    try:
        await ctx.send("In the near future, this command is going to give information about the bot and its developers.")
    except Exception as e:
        print(f"An erro occurred: {e}")
    print(f"About: completed at {datetime.now()}")



### use this token to test changes in test discord server ###
bot.run(TEST_TOKEN)

### use this token for deploying changes to live bot ###
# bot.run(DISCORD_TOKEN)

