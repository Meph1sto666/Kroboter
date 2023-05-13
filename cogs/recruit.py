import json
import discord
from discord.ext import commands
from discord.ui.item import Item
from lib.types.operator import *

class TagSelector(discord.ui.View):
	def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
		self.data:dict[str, dict[str, list[str]] | list[str] | list[dict[str, str | int | list[str]]]] = json.load(open("./data/recruitment.json", "r", encoding="utf-8"))
		self.operators:list[RecruitmentOp] = [RecruitmentOp(**o) for o in self.data.get("ops", [])] # type: ignore
		self.selectedTags:dict[str, list[str]] = {}
		self.selectedTagList:list[str] = []
		self.selects:list[discord.ui.Select[discord.ComponentType.string_select]] = [ # type: ignore
			discord.ui.Select(
				select_type=discord.ComponentType.string_select,
				custom_id=str(i),
				placeholder=str(i),
				min_values=0,
				max_values=min([5, len(self.data["grouped_tags"][i])]), # type: ignore
				options=[
					discord.SelectOption(
						label=str(t),
						value=str(t),
						default=str(t) in self.selectedTagList
					) for t in list(self.data["grouped_tags"][i]) # type: ignore
				]
			) for i in self.data["grouped_tags"]
		]
		for s in self.selects: # type: ignore
			if s.custom_id=="class": s.callback = self.tagCb # type: ignore
			self.add_item(s) # type: ignore
	async def tagCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		options:list[str] = []
		for s in self.selects: # type: ignore
			options.extend(filter(lambda x: not x in options or not x in self.selectedTagList, s.values)) # type: ignore
		print(options, self.selectedTagList)
		self.selectedTagList.extend(options)
		print("selectedTagsListPreRMV: " + self.selectedTagList.__str__())
		for t in self.selectedTagList:
			if t not in options:
				self.selectedTagList.remove(t)
		print("selectedTagsList: " + self.selectedTagList.__str__())
		for s in self.selects: # type: ignore
			# s.max_values = min(min(5-len(self.selectedTagList),len(self.selectedTagList)), len(s.options))
			for o in s.options: o.default = o.value in self.selectedTagList
		await interaction.response.edit_message(view=self)	
		

class RecruitCog(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot
		# ctx.respond(view=TagSelector())
	@discord.slash_command(name="reqruit", description="reqruitment tag filter") # type: ignore
	async def recruitCb(self, ctx:discord.Message) -> None:
		await ctx.respond(view=TagSelector())  # type: ignore


def setup(bot:discord.Bot) -> None:
    bot.add_cog(RecruitCog(bot))