import discord
from discord.ui.input_text import InputText
from datetime import datetime as dt

class DatePicker(discord.ui.Modal):
	def __init__(self, date:dt|None=None,*children: InputText, custom_id: str | None = None, timeout: float | None = None) -> None:
		super().__init__(*children, title="Date Picker", custom_id=custom_id, timeout=timeout)
		self.date:dt|None = None
		self.inputs: list[InputText] = [ # 
			discord.ui.InputText(
				custom_id="day",
				label="Day",
				placeholder="Input the day (1-31)",
				max_length=2,
				value=str(date.day) if date != None else None
			),
			discord.ui.InputText(
				custom_id="month",
				label="Month",
				placeholder="Input the month (1-12)",
				max_length=2,
				value=str(date.month) if date != None else None
			),
			discord.ui.InputText(
				custom_id="year",
				label="Year",
				placeholder="Input the Year",
				min_length=4,
				max_length=4,
				value=str(date.year if date != None else dt.now().year)
			)
		]
		for i in self.inputs:
			self.add_item(i)
	
	async def callback(self, interaction:discord.Interaction) -> None:
		await interaction.response.defer()