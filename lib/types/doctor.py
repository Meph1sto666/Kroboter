from datetime import datetime as dt
from lib.types.operator import *


class Profile:
	def __init__(self, display_name: str, friend_code: str, level: int | None, server: str | None, onboard: str | None, assistant: str | None, supports: list[dict[str, str | int | None | list[int]]] | None) -> None:
		self.name: str = display_name
		self.code: str = friend_code
		self.level: int = level if level != None else 0
		self.server: str | None = server
		self.onboard: dt | None = dt.fromisoformat(onboard) if onboard != None else None
		self.assistant: str | None = assistant
		self.supports: list[Operator] = [Operator(**s) for s in supports] if supports != None else [] # type: ignore

	def getLookupUrl(self) -> str:
		return getRoute("lookup", {"username": self.name})
	
	def createProfileEmbed(self) -> discord.Embed:
		prfEmbed: discord.Embed = discord.Embed(
			color=discord.Colour.from_rgb(*textToColor(self.name)),
			title=self.name,
			url=self.getLookupUrl(),
			timestamp=dt.now(),
			fields=[
				discord.EmbedField(name="level".upper(), value=str(self.level),inline=True),
				discord.EmbedField(name="server".upper(), value=self.server if self.server else "N/A",inline=True),
				discord.EmbedField(name="friend code".upper(), value=self.code,inline=True),
				discord.EmbedField(name="onboard".upper(), value=self.onboard.strftime("%Y-%m-%d") if self.onboard != None else "N/A",inline=True),
				discord.EmbedField(name="assistant".upper(), value=getOperatorNameById(self.assistant),inline=True)
			]
		)
		prfEmbed.set_footer(text="Fetched from Krooster API v1")
		return prfEmbed
  
	def createSupportSummary(self) -> discord.Embed:
		summary = discord.Embed(
			color=discord.Colour.from_rgb(*textToColor(self.name)),
			title="Support summary",
			# url=self.getLookupUrl(),
			timestamp=dt.now(),
			fields=[
				discord.EmbedField(
					name=f"{getOperatorNameById(s.id)}, E{s.elite} LV{s.level}",
					value=s.summary()
				) for s in self.supports
			]
		)
		return summary