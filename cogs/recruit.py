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
		self.sTags:list[str] = []
		self.selects:list[discord.ui.Select[discord.ComponentType.string_select]] = [ # type: ignore
			discord.ui.Select(
				custom_id=str(i),
				placeholder=str(i),
				min_values=0,
				max_values=min([5, len(self.data["grouped_tags"][i])]), # type: ignore
				options=[
					discord.SelectOption(
						label=str(t),
						value=str(t),
						default=str(t) in self.sTags
					) for t in list(self.data["grouped_tags"][i]) # type: ignore
				]
			) for i in self.data["grouped_tags"]
		]
		for s in self.selects: # type: ignore
			s.callback = self.tagCb # type: ignore
			self.add_item(s) # type: ignore
	async def tagCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		options:list[str] = []
		for s in self.selects: # type: ignore
			options.extend(filter(lambda x: not x in options, s.values)) # type: ignore
		self.sTags.extend(filter(lambda x: not x in self.sTags, options))
		for t in self.sTags:
			if t not in options: self.sTags.remove(t)
		for s in self.selects: # type: ignore
			for o in s.options: o.default = o.value in self.sTags
		res: dict[str, list[RecruitmentOp]] = {}
		for o in self.operators:
			tagStrs: list[str] = o.createMatchingTagsStrs(self.sTags,self.data["grouped_tags"]["rarity"]) # type: ignore
			for ts in tagStrs:
				if res.get(ts) == None: res[ts] = []
				res[ts].append(o)
		try: res.pop("")
		except: pass
		# star:str = "\U00002B50"
		sR: list[list[int]] = [list(dict.fromkeys([i.rarity for i in res[r]]))for r in res]
		rarities:dict[str, list[tuple[str, tuple[int, int]]]] = dict([(list(res)[s],(min(sR[s]),max(sR[s]))) for s in range(len(list(res)))])
		res = dict(sorted(res.items(), key=lambda x: (len(x[1]), max([o.rarity for o in x[1]]))))
		print([max([o.rarity for o in x[1]]) for x in res.items()])
		await interaction.response.edit_message(view=self, embed=discord.Embed(
			title="Recruitment results",
			timestamp=dt.now(),
			fields=[discord.EmbedField(inline=False,name=f"{r} [{f'{rarities[r][0]} - {rarities[r][1]}' if (rarities[r][0]!=rarities[r][1]) else f'{rarities[r][0]}'}]",value=", ".join([f"`{o.name}`"for o in res[r]]))for r in res]
			# fields=[discord.EmbedField(inline=False,name=f"{r} [{', '.join([str(a)+star for a in list(dict.fromkeys(sorted([i.rarity for i in res[r]],reverse=True)))])}]",value=" ".join([f"`{o.name}`"for o in res[r]]))for r in res]
		))
		

class RecruitCog(commands.Cog):
	def __init__(self, bot:discord.Bot) -> None:
		super().__init__()
		self.bot:discord.Bot = bot
	@discord.slash_command(name="reqruit", description="reqruitment tag filter") # type: ignore
	async def recruitCb(self, ctx:discord.Message) -> None:
		await ctx.respond(view=TagSelector())  # type: ignore


def setup(bot:discord.Bot) -> None:
    bot.add_cog(RecruitCog(bot))