import discord
from discord.ext import commands
import asyncio
import json

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    bot_token = config_data.get('token')

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
async def countdown(ctx, arg):
    print("Countdown: executing")
    start_countdown_from = 10
    if arg.isnumeric():
        start_countdown_from = int(arg) > 10 if 10 else int(arg)
    try:
        for i in range(start_countdown_from, 0, -1):
            await ctx.send(f"{i}...")
            await asyncio.sleep(1)
        await ctx.send("GOOOOOOOOOOOOO!")
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




bot.run(bot_token)
