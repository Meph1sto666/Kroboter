# import requests
import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *
from lib.paginator import *


class ProfileCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="profile", description="returns the users profile") # type: ignore
	async def profileCbv1(self, ctx: discord.Message, username: str) -> None:
		# url: str = getRoute("v1_u_profile", {"username": username})
		lookupUrl:str = getRoute("lookup", {"username": username})
		# res: requests.Response = requests.api.get(url) # type: ignore
		# if res.status_code == 204: raise UserDoesNotExist(username) # type: ignore
		# res.raise_for_status() # type: ignore
		# userProfile = Profile(**res.json())  # type: ignore
		userProfile = Profile("Meph1sto666", "Meph1sto666#6039", 70, "EN", "2022-09-18", "char_474_glady", [
			Operator("char_275_breeze", True, True, 2, 2, 60, 7, [0,1], [2], None).__dict__,
			Operator("char_017_huang", True, True, 1, 2, 60, 7, [0,2,0], [], None).__dict__,
			Operator("char_377_gdglow", True, True, 1, 2, 60, 7, [2,1,3], [], None).__dict__,
		])
		prfEmbed: discord.Embed = discord.Embed(
			color=discord.Colour.from_rgb(*textToColor(userProfile.name)),
			title=userProfile.name,
			url=lookupUrl,
			timestamp=dt.now(),
			fields=[
				discord.EmbedField(name="level".upper(), value=str(userProfile.level),inline=True),
				discord.EmbedField(name="server".upper(), value=userProfile.server if userProfile.server else "N/A",inline=True),
				discord.EmbedField(name="friend code".upper(), value=userProfile.code,inline=True),
				discord.EmbedField(name="onboard".upper(), value=userProfile.onboard.strftime("%Y-%m-%d") if userProfile.onboard != None else "N/A",inline=True),
				discord.EmbedField(name="assistant".upper(), value=getOperatorNameById(userProfile.assistant),inline=True)
			]
		)
		prfEmbed.set_footer(text="Fetched from Krooster API v1")
		supports: list[discord.Embed] = [userProfile.supports[s].createEmbed(lookupUrl, f"support unit {s+1}".upper()) for s in range(len(userProfile.supports))]
		# await ctx.respond(embeds=[prfEmbed,*supports])  # type: ignore
		p:Paginator = Paginator(ctx, supports, [prfEmbed])
		await p.send()

	@profileCbv1.error # type: ignore
	async def profileCmdErrorCb(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		await ctx.respond(f"```{error.with_traceback(error.__traceback__)}```") # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(ProfileCog(bot))
