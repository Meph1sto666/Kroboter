import requests
import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *


class ProfileCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot

	@discord.slash_command(name="profile", description="returns the users profile") # type: ignore
	async def profileCbv1(self, ctx: discord.Message, username: str) -> None:
		url: str = getRoute("v1_u_profile", {"username": username})
		res: requests.Response = requests.api.get(url) # type: ignore
		if res.status_code == 204: raise UserDoesNotExist(username) # type: ignore
		res.raise_for_status() # type: ignore
		userProfile = Profile(**res.json())  # type: ignore
		userProfile = Profile("Meph1sto666", "Meph1sto666#1854", 69, "EN", "2022-09-18", "char_017_huang", [{"op_id":"char_275_breeze", "op_skill":7, "op_module":2},{"op_id":"char_017_huang", "op_skill":7},{"op_id":"char_377_gdglow", "op_skill":7}])
		fields:list[discord.EmbedField] = [
			discord.EmbedField(name="Name", value=userProfile.name),
			discord.EmbedField(name="Friend code", value=userProfile.code),
			discord.EmbedField(name="Level", value=str(userProfile.level[0])),
			discord.EmbedField(name="Server", value=userProfile.server if userProfile.server else "N/A"),
			discord.EmbedField(name="Onboard", value=userProfile.onboard.isoformat() if userProfile.onboard != None else "N/A"),
			discord.EmbedField(name="Assistant", value=getOperatorNameFromId(userProfile.assistant))
		]
		if userProfile.supports != None:
			fields.extend([discord.EmbedField(
					name=f"Support {s}",
					value=userProfile.supports[s].__str__()
    			) for s in range(len(userProfile.supports))]
			)
		prfEmbed: discord.Embed = discord.Embed(
			color=discord.Colour.from_rgb(0, 255, 0),
			title=userProfile.name,
			url=url,
			timestamp=dt.now(),
			fields=fields
		)
		prfEmbed.set_footer(text="Fetched from Krooster API v1")
		await ctx.respond(embed=prfEmbed)  # type: ignore

	@profileCbv1.error # type: ignore
	async def profileCmdErrorCb(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		await ctx.respond(f"```{error.__traceback__}```") # type: ignore


def setup(bot: discord.Bot) -> None:
	bot.add_cog(ProfileCog(bot))
