from discord.interactions import Interaction
from discord.ui.input_text import InputText
from discord.ui.item import Item
import discord
from discord.ext import commands
from lib.connections import *
from lib.types.doctor import *
from lib.types.operator import *
		
class UnitSelectView(discord.ui.View):
	def __init__(self, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: #type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) #type: ignore
		self.servers:dict[str, dict[str, str | bool]] = dict(json.load(open("./data/servers.json")))
		# selected attributes
		self.operatorId:str|None = None
		self.classTag:str|None = None
		self.rarity:int = 0
		self.cnServer:bool = False
		# base data
		self.operators:dict[str, dict[str, str | int | list[dict[str, str]] | list[dict[str, str | bool]] | list[str]]] = json.load(open("./data/operators.json", encoding="utf-8"))
		self.classTags:list[str] = json.load(open("./data/classtags.json", encoding="utf-8"))
		# select menus
		self.raritySelect:discord.ui.Select = discord.ui.Select(custom_id="rarity",placeholder="Select Operator rarity",options=self.editSelects()[0],row=1) # type: ignore
		self.classSelect:discord.ui.Select = discord.ui.Select(custom_id="class",placeholder="Select Operator class",options=self.editSelects()[1],row=2) # type: ignore
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
			[discord.SelectOption(label=str(self.servers[s].get('abb')).upper(), value=s, description=str(self.servers[s].get('name')), default=bool(self.servers[s].get("default", False))) for s in self.servers]
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
		op:str|None = interaction.data.get("values", [None])[0]
		if op == None: return
		self.operatorId = op
		await interaction.response.edit_message(view=UnitPSMSelectView(self))

	def filterOps(self) -> list[dict[str, str | int | list[dict[str, str]] | list[dict[str, str | bool]] | list[str]]]:
		return list(filter(lambda x:x["rarity"]==self.rarity and x["class"]==self.classTag and(not x.get("isCnOnly",False) if not self.cnServer else True),list(self.operators.values())))
	def createOperatorOptions(self) -> list[discord.SelectOption]:
		ops: list[discord.SelectOption] = [discord.SelectOption(label=str(o.get("name")), value=str(o.get("id")), description=f"{o.get('id', str(None))} ") for o in self.filterOps()]
		ops.sort(key=lambda x: x.label)
		if len(ops) < 1: ops.append(discord.SelectOption(label="None", value="none", description="No operators found"))
		return ops

class UnitPSMSelectView(discord.ui.View):
	def __init__(self, unitSelector:UnitSelectView, *items: Item, timeout: float | None = 180, disable_on_timeout: bool = False) -> None: # type: ignore
		super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout) # type: ignore
		self.unitSelector:UnitSelectView = unitSelector
		self.unitData:dict[str, list[dict[str, str]]] = dict(json.load(open("./data/operators.json"))).get(self.unitSelector.operatorId, {})
		self.raritySpecs:dict[str, list[int]] = dict(json.load(open("./data/rarityspecs.json"))).get(str(self.unitData.get("rarity")), {})
		self.modules = list(filter(lambda x: x.get("isCnOnly")==self.unitData.get("isCnOnly"),self.unitData.get("modules", [{"moduleName":None, "moduleId":None}])))
		self.searchData = {
			"op_id": self.unitSelector.operatorId,
			"skill": None,
			"potential": 0,
			"module": None,
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
			placeholder="Select a potential",
			options=[discord.SelectOption(label=str(s.get("pot_name", "<pot_id>")), value=str(s.get("pot_id", "<pot_id>")), description=str(int(s.get("pot_id",-1))+1)) for s in [{"pot_id": p-1,"pot_name":potData[p]} for p in range(len(potData))]]
		)
		self.moduleSelect:discord.SelectMenu|None = None
		if len(self.modules) > 0:
			self.moduleSelect = discord.ui.Select( # type: ignore
				custom_id="module",
				placeholder="Select a module",
				options=[discord.SelectOption(label=f"Module {m+1}", value=str(m), description=self.modules[m].get("moduleName", "<mod_name>")) for m in range(len(self.modules))]
			)
		self.backBtn:discord.Button = discord.ui.Button( # type: ignore
			style=discord.ButtonStyle.danger,
			label="EDIT OPERATOR",
			custom_id="back_btn"
		)

		self.skillSelect.callback = self.defaultSelectCb
		self.potSelect.callback = self.defaultSelectCb
		self.backBtn.callback = self.backBtnCb
		self.doneBtn.callback = self.doneBtnCb
		# add items menus
		self.add_item(self.skillSelect) # type: ignore
		self.add_item(self.potSelect) # type: ignore
		if self.moduleSelect != None:
			self.moduleSelect.callback = self.defaultSelectCb
			self.add_item(self.moduleSelect) # type: ignore
		self.add_item(self.backBtn) # type: ignore
		self.add_item(self.doneBtn) # type: ignore
		
	async def backBtnCb(self, interaction:discord.Interaction) -> None:
		await interaction.response.edit_message(view=self.unitSelector)
		del self
	"""
	async def skillCb(self, interaction:discord.Interaction) -> None: # not doing shit yet
		if interaction.data == None: return
		# v:str|None = interaction.data.get("values", [None])[0]
		await interaction.response.defer()
	async def potCb(self, interaction:discord.Interaction) -> None: # not doing shit yet
		if interaction.data == None: return
		self.searchData["potential"] = interaction.data.get("values", [None])[0]
		await interaction.response.defer()
	"""
	async def defaultSelectCb(self, interaction:discord.Interaction) -> None:
		if interaction.data == None: return
		self.searchData[str(interaction.custom_id)] = interaction.data.get("values", [None])[0]
		await interaction.response.defer()

	async def doneBtnCb(self, interaction:discord.Interaction) -> None:
		self.modal=UnitSpecsModal(self, title="")
		await interaction.response.send_modal(modal=self.modal)
		await self.modal.wait()
		data:dict[str, int] = {}
		for c in self.modal.children:
			if c.value == None: continue
			if not c.value.isdigit(): continue
			v:int = int(c.value)
			cSpecs: list[int] = self.raritySpecs.get(c.custom_id, [])
			if v < cSpecs[0]: v = cSpecs[0]
			if not c.custom_id == "level":
				if v > cSpecs[1]: v = cSpecs[1]
			else:
				if v > cSpecs[data.get("elite",0)+1]: v = cSpecs[data.get("elite",0)+1]
			data[c.custom_id] = v
		self.searchData: dict[str, str | int | None] = {**self.searchData, **data}
		print(self.searchData)
		self.modal.stop()
			
class UnitSpecsModal(discord.ui.Modal):
	def __init__(self, psmSelect:UnitPSMSelectView, *children: InputText, title: str, custom_id: str | None = None, timeout: float | None = None) -> None:
		super().__init__(*children, title=title, custom_id=custom_id, timeout=timeout)
		self.psmSelector: UnitPSMSelectView = psmSelect
		self.title = f"Input search specifications for {self.psmSelector.unitData.get('name')}."
		self.minEliteInp = discord.ui.InputText(custom_id="elite", label="Promotion", placeholder="Input promotion level (0-2)", min_length=0, max_length=1, required=False, value="0")
		self.minLvlInp = discord.ui.InputText(custom_id="level", label="Level", placeholder="Input level (1-90)", min_length=0, max_length=2, required=False)
		self.minSkillRankInp = discord.ui.InputText(custom_id="rank", label="Rank", placeholder="Input skill rank (1-7)", min_length=0, max_length=1, required=False)
		self.minSkillMasteryInp = discord.ui.InputText(custom_id="mastery", label="Mastery", placeholder="Input skill mastery level (1-3)", min_length=0, max_length=1, required=False)
		self.minModuleStageInp:discord.ui.InputText|None = None
		if len(self.psmSelector.modules) > 0:
			self.minModuleStageInp = discord.ui.InputText(custom_id="stage", label="Stage", placeholder="Input module stage (1-3)", min_length=0, max_length=1, required=False)
		self.add_item(self.minEliteInp)
		self.add_item(self.minLvlInp)
		self.add_item(self.minSkillRankInp)
		self.add_item(self.minSkillMasteryInp)
		if self.minModuleStageInp != None: self.add_item(self.minModuleStageInp)

	async def callback(self, interaction: Interaction) -> None:
		await interaction.response.defer()

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