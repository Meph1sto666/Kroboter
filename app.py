import os;
import discord
from dotenv import load_dotenv
from packages import logger
logger.init()

load_dotenv()
bot = discord.Bot()




bot.run(token=os.getenv("TOKEN"))