from discord.ui.item import Item
import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *

class UnitSelectView(discord.ui.View):
	def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: #type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) #type: ignore
		self.classTag:str|None = None
		self.rarity:int = 0

	# def editClassSelector(self, interaction:discord.Interaction) -> None:
	# 	# className:str = interaction.get(...)
	# 	jsonDta:dict[str, str | int] = dict(json.load(open("./data/operators.json")))
		

class LookupCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="search", description="returns the users profile") # type: ignore
	async def profileCbv1(self, ctx: discord.Message, username: str) -> None:
		
		await ctx.respond(embed=prfEmbed)  # type: ignore

	@profileCbv1.error # type: ignore
	async def profileCmdErrorCb(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		await ctx.respond(f"```{error.__traceback__}```") # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(LookupCog(bot))