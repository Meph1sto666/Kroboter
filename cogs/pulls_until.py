import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *
from lib.paginator import *
from lib.supportpaginator import *
from datetime import datetime as dt


class PullsUntilCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="pulls_until", description="calculates the amount of pulls from start to end date") # type: ignore
	async def profileCbv1(self, ctx: discord.Message, end:str, start:str|None=None) -> None:
		if start == None: self.start:dt = dt.now()
		else: self.start = dt.fromisoformat(str(start))
		self.end:dt = dt.fromisoformat(str(start))

	@profileCbv1.error # type: ignore
	async def profileCmdErrorCb(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(PullsUntilCog(bot))
