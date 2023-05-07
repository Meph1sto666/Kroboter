import discord
from discord.ui.item import Item

class Paginator:
	def __init__(self, ctx:discord.Message, pages:list[discord.Embed], constantPages:list[discord.Embed]=[], ephemeral:bool=False) -> None:
		self.pageIndex:int = 0
		self.constantPages:list[discord.Embed] = constantPages
		self.pages:list[discord.Embed] = pages
		self.controls:PaginatorOptions = PaginatorOptions(self)
		self.ctx:discord.Message = ctx
		self.ephemeral:bool = ephemeral

	def prevPage(self) -> discord.Embed:
		if not self.pageIndex-1 < 0: self.pageIndex-=1
		return self.pages[self.pageIndex]
	def nextPage(self) -> discord.Embed:
		if not self.pageIndex+1 > len(self.pages): self.pageIndex+=1
		return self.pages[self.pageIndex]
	def getPage(self, index:int=-1) -> discord.Embed:
		return self.pages[self.pageIndex if index < 0 else index]
	async def send(self) -> None:
		await self.ctx.respond(content=f"{self.pageIndex+1} / {len(self.pages)}", embeds=[*self.constantPages, self.getPage()], view=self.controls, ephemeral=self.ephemeral) # type: ignore
	async def update(self) -> None:
		if len(self.pages) <= self.pageIndex: self.pageIndex = len(self.pages)-1
		self.updateButtons()
		await self.ctx.edit(content=f"{self.pageIndex+1} / {len(self.pages)}", embeds=[*self.constantPages, self.getPage()], view=self.controls)
	def addPage(self, page:discord.Embed, index:int|None=None) -> None:
		self.pages.insert(index if index != None else len(self.pages), page)
	def editPage(self, index:int, edited:discord.Embed) -> None:
		if index >= len(self.pages): return
		self.pages[index] = edited
	def removePage(self, index:int) -> None:
		if index >= len(self.pages): return
		self.pages.pop(index)
	def updateButtons(self) -> None:
		self.controls.get_item("prev_btn").disabled = len(self.pages) < 1 or self.pageIndex < 1 # type: ignore
		self.controls.get_item("next_btn").disabled = len(self.pages) < 1 or self.pageIndex+1 >= len(self.pages) # type: ignore

class PaginatorOptions(discord.ui.View):
	def __init__(self, parent:Paginator, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
		self.parent:Paginator = parent

	@discord.ui.button(label="\U00002B05 BACK",style=discord.ButtonStyle.blurple, custom_id="prev_btn") # type: ignore
	async def cb_tts_prev_btn(self, button:discord.Button, interaction:discord.Interaction) -> None:
		self.parent.prevPage()
		self.parent.updateButtons()
		await interaction.response.defer()
		await self.parent.update()
	@discord.ui.button(label="NEXT \U000027A1", style=discord.ButtonStyle.blurple, custom_id="next_btn") # type: ignore
	async def cb_tts_next_btn(self, button:discord.Button, interaction:discord.Interaction) -> None:
		self.parent.nextPage()
		self.parent.updateButtons()
		await interaction.response.defer()
		await self.parent.update()