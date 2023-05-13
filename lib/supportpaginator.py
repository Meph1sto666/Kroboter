import discord
from discord.ui.item import Item

class SupportPaginator:
	def __init__(self, ctx:discord.Message, pages:list[discord.Embed], constantPages:list[discord.Embed]=[], ephemeral:bool=False) -> None:
		self.pageIndex:int = 0
		self.constantPages:list[discord.Embed] = constantPages
		self.pages:list[discord.Embed] = pages
		self.controls:SupportPaginatorOptions = SupportPaginatorOptions(self)
		self.ctx:discord.Message = ctx
		self.ephemeral:bool = ephemeral

	def getPage(self, index:int|None=None) -> discord.Embed:
		return self.pages[self.pageIndex if index == None else index]
	async def send(self) -> None:
		self.updateButtons()
		await self.ctx.respond(embeds=[*self.constantPages, self.getPage()], view=self.controls, ephemeral=self.ephemeral) # type: ignore
	async def update(self) -> None:
		self.updateButtons()
		await self.ctx.edit(embeds=[*self.constantPages, self.getPage()], view=self.controls)
	def updateButtons(self) -> None:
		for b in self.controls.children: b.disabled = False # type: ignore
		self.controls.get_item(str(self.pageIndex)).disabled = True # type: ignore
		
class SupportPaginatorOptions(discord.ui.View):
	def __init__(self, parent:SupportPaginator, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
		self.parent:SupportPaginator = parent
		self.createBaseControls()

	def createBaseControls(self) -> None:
		emojis:list[str] = ["\U0001F4CB", "\U00000031", "\U00000032", "\U00000033"]
		for i in range(len(self.parent.pages)):
			btn = discord.ui.Button( # type: ignore
				label=emojis[i],
				style=discord.ButtonStyle.blurple,
				custom_id=str(i)
			)
			btn.callback = self.control_cb # type: ignore
			self.add_item(btn) # type: ignore
	async def control_cb(self, interaction:discord.Interaction) -> None:
		self.parent.pageIndex=int(interaction.data.get("custom_id", 0)) # type: ignore
		await interaction.response.defer()
		await self.parent.update()
