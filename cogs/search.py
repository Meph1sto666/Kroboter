from discord.ui.input_text import InputText
from discord.ui.item import Item
import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *

class UnitSpecsModal(discord.ui.Modal):
	def __init__(self, opData:dict[str, list[dict[str, str]]], *children: InputText, title: str, custom_id: str | None = None, timeout: float | None = None) -> None:
		super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
		self.title = f"Search specifications for {opData.get('name')}"
		# self.minLvl = discord.ui.InputText(label="minLvl")
		# self.add_item(self.minLvl)

class UnitPSMSelectView(discord.ui.View):
	def __init__(self, operatorId:str, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
		self.unitData:dict[str, list[dict[str, str]]] = dict(json.load(open("./data/operators.json"))).get(operatorId, {})
		self.searchData = {
			"op_id": operatorId,
			"skill": None,
			"skill_lvl": 0,
			"potential": 0,
			"module": None,
			"module_stage": 0
		}
		# temp data
		potData:list[str] = self.unitData.get("potentials", [""]) # type: ignore
		potData.insert(0, "None") # type: ignore
		skillData:list[dict[str,str]] = self.unitData.get("skills", [])
		# buttons
		self.doneBtn:discord.Button = discord.ui.Button( # type: ignore
			style=discord.ButtonStyle.green,
			label="Done",
			custom_id="done"
		)
		# select menus
		self.skillSelect:discord.SelectMenu = discord.ui.Select( # type: ignore
			custom_id="skill",
			placeholder="Select a skill",
			options=[discord.SelectOption(label=f"Skill {s+1}", description=skillData[s].get("skillName", "<skill_name>"), value=skillData[s].get("skillId", "<skill_id>")) for s in range(len(skillData))]
		)
		self.potSelect:discord.SelectMenu = discord.ui.Select( # type: ignore
			custom_id="potential",
			placeholder="Select a minimum potential",
			options=[discord.SelectOption(label=str(s.get("pot_name", "<pot_id>")), value=str(s.get("pot_id", "<pot_id>")), description=str(int(s.get("pot_id",-1))+1)) for s in [{"pot_id": p-1,"pot_name":potData[p]} for p in range(len(potData))]]
		)
		modules = list(filter(lambda x: x.get("isCnOnly")==self.unitData.get("isCnOnly"),self.unitData.get("modules", [{"moduleName":None, "moduleId":None}])))
		self.moduleSelect:discord.SelectMenu|None = None
		if len(modules) > 0:
			self.moduleSelect = discord.ui.Select( # type: ignore
				custom_id="module",
				placeholder="Select a module",
				options=[discord.SelectOption(label=f"Module {m+1}", value=str(m), description=modules[m].get("moduleName", "<mod_name>")) for m in range(len(modules))]
			)
			self.moduleStageSelect = discord.ui.Select( # type: ignore
				custom_id="module_stage",
				placeholder="Select the stage",
				options=[discord.SelectOption(label=f"Stage {s+1}", value=str(s+1)) for s in range(3)]
			)

		self.skillSelect.callback = self.skillCb
		self.potSelect.callback = self.potCb
		self.doneBtn.callback = self.doneBtnCb
		# add items menus
		self.add_item(self.skillSelect) # type: ignore
		self.add_item(self.potSelect) # type: ignore
		if self.moduleSelect != None:
			self.add_item(self.moduleSelect) # type: ignore
		self.add_item(self.doneBtn) # type: ignore
		
	async def skillCb(self, interaction:discord.Interaction):
		if interaction.data == None: return
		# v:str|None = interaction.data.get("values", [None])[0]
		await interaction.response.defer()

	async def potCb(self, interaction:discord.Interaction):
		if interaction.data == None: return
		interaction.data.get("values", [None])[0]
		await interaction.response.defer()
	async def doneBtnCb(self, interaction:discord.Interaction):
		# await interaction.response.send_message("^^")
		await interaction.response.send_modal(modal=UnitSpecsModal(self.unitData, title=""))

		
class UnitSelectView(discord.ui.View):
	def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: #type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) #type: ignore
		# selected attributes
		self.classTag:str|None = None
		self.rarity:int = 0
		self.cnServer:bool = False
		# base data
		self.operators:dict[str, dict[str, str | int | list[dict[str, str]] | list[dict[str, str | bool]] | list[str]]] = json.load(open("./data/operators.json", encoding="utf-8"))
		self.classTags:list[str] = json.load(open("./data/classtags.json", encoding="utf-8"))
		# select menus
		self.raritySelect:discord.ui.Select = discord.ui.Select(custom_id="rarity",placeholder="Select Oerator rarity",options=self.editSelects()[0],row=1) # type: ignore
		self.classSelect:discord.ui.Select = discord.ui.Select(custom_id="class",placeholder="Select Oerator class",options=self.editSelects()[1],row=2) # type: ignore
		self.serverSelect:discord.ui.Select = discord.ui.Select(custom_id="server",placeholder="Select a server",options=self.editSelects()[2],row=3) # type: ignore
		self.operatorSelect:discord.ui.Select = discord.ui.Select(custom_id="operator",placeholder="Select an operator",options=self.createOperatorOptions()[:25],row=4) # type: ignore
		# set callbacks and add menus
		self.raritySelect.callback = self.raritySelectCb # type: ignore
		self.classSelect.callback = self.classSelectCb # type: ignore
		self.serverSelect.callback = self.serverSelectCb # type: ignore
		self.operatorSelect.callback = self.operatorSelectCb # type: ignore
		for i in [self.raritySelect, self.classSelect, self.serverSelect, self.operatorSelect]: # type: ignore
			self.add_item(i) # type: ignore

	def editSelects(self) -> list[list[discord.SelectOption]]:
		options:list[list[discord.SelectOption]] = [
			[discord.SelectOption(label=str(s), value=str(s), description=f"{s}* Operator", default=(self.rarity==s)) for s in [1,2,3,4,5,6]],
			[discord.SelectOption(label=c, value=c, description=f"{c} Operator", default=(self.classTag!=None and self.classTag==c)) for c in self.classTags],
			[discord.SelectOption(label=s.upper(), value=s, description=f"{s.upper()} server", default=s=="en") for s in ["en", "cn"]]
		]
		try:
			self.raritySelect.options = options[0] # type: ignore
			self.classSelect.options = options[1] # type: ignore
			self.serverSelect.options = options[2] # type: ignore
		except:pass
		return options
		
	async def raritySelectCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		sel:str|None = interaction.data.get("values", [None])[0]
		self.rarity = int(sel if sel!=None else -1)
		self.operatorSelect.options = self.createOperatorOptions() # type: ignore
		self.editSelects()
		await interaction.response.edit_message(view=self)
	async def classSelectCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		self.classTag = interaction.data.get("values", [None])[0]
		self.operatorSelect.options = self.createOperatorOptions() # type: ignore
		self.editSelects()
		await interaction.response.edit_message(view=self)
	async def serverSelectCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		self.cnServer = interaction.data.get("values", [None])[0]=="cn"
		self.editSelects()
		self.operatorSelect.options = self.createOperatorOptions() # type: ignore
		await interaction.response.edit_message(view=self)
	async def operatorSelectCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		op:str = interaction.data.get("values", ["None"])[0]
		# await interaction.response.send_message(content=f"you selected: `{op}`")
		await interaction.response.edit_message(view=UnitPSMSelectView(op))

	def filterOps(self) -> list[dict[str, str | int | list[dict[str, str]] | list[dict[str, str | bool]] | list[str]]]:
		return list(filter(lambda x:x["rarity"]==self.rarity and x["class"]==self.classTag and(not x.get("isCnOnly",False) if not self.cnServer else True),list(self.operators.values())))
	def createOperatorOptions(self) -> list[discord.SelectOption]:
		ops: list[discord.SelectOption] = [discord.SelectOption(label=str(o.get("name")), value=str(o.get("id")), description=f"{o.get('id', str(None))} ") for o in self.filterOps()]
		ops.sort(key=lambda x: x.label)
		if len(ops) < 1: ops.append(discord.SelectOption(label="None", value="none", description="no operator"))
		return ops

class LookupCog(commands.Cog):
	def __init__(self, bot: discord.Bot) -> None:
		super().__init__()
		self.bot: discord.Bot = bot
	@discord.slash_command(name="search", description="searches krooster for matching support units") # type: ignore
	async def searchCbv1(self, ctx: discord.Message) -> None:
		await ctx.respond(view=UnitSelectView()) # type: ignore
	@searchCbv1.error # type: ignore
	async def profileCmdErrorCb(self, ctx:discord.Message, error:discord.ApplicationCommandError) -> None:
		raise error

def setup(bot: discord.Bot) -> None:
	bot.add_cog(LookupCog(bot))