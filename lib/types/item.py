class StageData:
	def __init__(self, type:str, cost:int, name:str, dropRate:float, itemPerSanity:float) -> None:
		"""Constructor

		Args:
			type (str): Type of the stage (most efficient / least sanity)
			cost (int): Stage costs
			name (str): Name of the stage
			dropRate (float): Droprate of the item
			itemPerSanity (float): Amount of sanity per item
		"""
		self.TYPE:str = type
		self.COSTS:int = cost
		self.NAME:str = name
		self.DROP_RATE:float = dropRate
		self.ITEM_P_SANITY:float = itemPerSanity

class Ingredient:
	def __init__(self, id:str, quantity:int) -> None:
		"""Constuctor

		Args:
			id (str): Ingredient ID
			quantity (int): Amount needed
		"""
		self.ID:str = id
		self.QUANTITY:int = quantity
	
	def __json__(self) -> dict[str, str | int]:
		return {
			"id": self.ID,
			"quantity": self.QUANTITY
		}

class Item:
	def __init__(self, id:str, name:str, iconId:str, tier:int, sortId:int, ingredients:list[Ingredient]|None=None, crop:int|None=None, stages:list[StageData]|None=None) -> None:
		"""Constructor

		Args:
			id (str): Item ID
			name (str): Item name
			iconId (str): ID of the icon
			tier (int): Item value
			sortId (int): ID for sorting
			ingredients (list[Ingredients] | None, optional): Ingredients required for crafting. Defaults to None.
			crop (int | None, optional): Amount yielded by crafting. Defaults to None.
			stages (list[StageData] | None, optional): Farm Stages. Defaults to None.
		"""
		self.ID:str = id
		self.NAME:str = name
		self.iconId:str = iconId
		self.tier:int = tier
		self.sorId:int = sortId
		self.ingredients:list[Ingredient] | None = ingredients
		self.crop:int | None = crop if ingredients != None else crop
		self.stages:list[StageData] | None = stages