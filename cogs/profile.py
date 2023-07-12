# import requests
import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *
from lib.paginator import *
from lib.supportpaginator import *


class ProfileCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="profile", description="returns the users profile") # type: ignore
	async def profileCbv1(self, ctx: discord.Message, username: str) -> None:
		# url: str = getRoute("v1_u_profile", {"username": username})
		# res: requests.Response = requests.api.get(url) # type: ignore
		# if res.status_code == 204: raise UserDoesNotExist(username) # type: ignore
		# res.raise_for_status() # type: ignore
		# userProfile = Profile(**res.json())  # type: ignore
		userProfile = Profile("Meph1sto666", "Meph1sto666#5670", 70, "EN", "2022-09-18", "char_474_glady", [
			Operator("char_275_breeze", True, True, 2, 2, 60, 7, [0,1], [2], None).__dict__,
			Operator("char_017_huang", True, True, 1, 2, 60, 7, [0,2,0], [], None).__dict__,
			Operator("char_377_gdglow", True, True, 1, 2, 60, 7, [2,1,3], [], None).__dict__,
		])
		supports: list[discord.Embed] = [userProfile.supports[s].createEmbed(userProfile.getLookupUrl(), f"support unit {s+1}".upper()) for s in range(len(userProfile.supports))]
		supports.insert(0, userProfile.createSupportSummary())
		p:SupportPaginator = SupportPaginator(ctx, supports, [userProfile.createProfileEmbed()])
		print(p.pages[0].title)
		await p.send()

	@profileCbv1.error # type: ignore
	async def profileCmdErrorCb(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(ProfileCog(bot))
