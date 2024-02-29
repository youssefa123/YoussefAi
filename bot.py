from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime

BOT_TOKEN = "MTIxMjgxOTQzNjM4MjQ1Mzc5MQ.GI3Obi.z_mPzaH4yoLXUnHog3XtB9Hc7Lo0vK7YY7FWpw"
CHANNEL_ID = 1212826646973911091
MAX_SESSION_TIME_MINUTES = 30



@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) #Uses all feautures of discord.py
session = Session()

@bot.event
async def on_ready():
    print("Hello, Study bot is ready.")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello, I am ready to help you study!")

@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2) 
async def remind_user():
    #ignores the first count
    if remind_user.current_loop == 0:
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("You have been studying for 30 minutes. Take a break!")


@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()

    #Easier to read time
    human_readable_time = ctx.message.created_at.strftime("%H:%M")
    remind_user.start()
    await ctx.send(f"You started at {human_readable_time} ")


@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No active session")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration_seconds = int(end_time - session.start_time)

    #Easier to read time
    hours, remainder = divmod(duration_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    #formating string based on duration
    if hours:
        human_readable_time = f"{hours} hours, {minutes} minutes and {seconds} seconds"
    elif minutes:
        human_readable_time = f"{minutes} minutes and {seconds} seconds"
    else:
        human_readable_time = f"{seconds} seconds"
    remind_user.stop()
    await ctx.send(f"Session ended. You studied for {human_readable_time}")


bot.run(BOT_TOKEN)

