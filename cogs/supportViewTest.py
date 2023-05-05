import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *


class supTestCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="support_emb_test", description="returns an embed") # type: ignore
	async def profileCbv1(self, ctx: discord.Message, username: str) -> None:
		url: str = getRoute("lookup", {"username": username})
		# su1 = SupportUnit("char_340_shwaz", 7, 3)
		# su2 = SupportUnit("char_213_mostma", 7, 3)
		a: list[Operator] = [
			Operator("char_377_gdglow", True, True, 1, 2, 60, 7, [0,0,3], [], None),
			Operator("char_017_huang", True, True, 1, 2, 60, 7, [0,2,0], [], None),
			Operator("char_118_yuki", True, True, 6, 2, 40, 7, [0,2], [3], None),
			Operator("char_275_breeze", True, True, 2, 2, 60, 7, [0,1], [2], None),
			Operator("char_474_glady", True, True, 2, 2, 60, 7, [0,0,1], [1], None),
			Operator("char_103_angel", True, True, 2, 2, 60, 7, [0,0,0], [1], None),
			Operator("char_4042_lumen", True, True, 2, 2, 20, 7, [0,0,0], [0], None)
		]
		await ctx.respond(embeds=[o.createEmbed(url, username) for o in a]) # type: ignore

		


def setup(bot: discord.Bot) -> None:
	bot.add_cog(supTestCog(bot))
