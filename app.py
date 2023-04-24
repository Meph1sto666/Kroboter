import os
import discord
from dotenv import load_dotenv # type: ignore
from lib.settings import LOGGING_CNFG #type: ignore
load_dotenv()

bot = discord.Bot()
intents:discord.Intents = discord.Intents.all()
intents.members = True;

def addCogs(path:str) -> None:
    if "__pycache__" in path: return
    if os.path.isdir(path):
        for p in os.listdir(path):
            addCogs(f"{path}/{p}")
    else:
        bot.load_extension(path[2:-3].replace("/", "."))
addCogs("./cogs")

bot.run(token=os.getenv("TOKEN"), reconnect=True)