import discord
from discord.ext import commands

class ProfileCog(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__() 
		self.bot: discord.Bot = bot

	@discord.slash_command(name="test", description="cog test cmd") #type: ignore
	async def res(self, ctx:discord.Message) -> None:
		await ctx.respond("abawfoawpofj", ephemeral=True) #type: ignore

def setup(bot:discord.Bot) -> None:
	bot.add_cog(ProfileCog(bot))