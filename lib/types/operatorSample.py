import json
from lib.types import item
OPERATOR_FILE = "./data/operators.json"

class Skin:
	def __init__(self, skinId:str, skinName:str|None, sortId:int) -> None:
		self.ID:str = skinId
		self.NAME:str|None = skinName
		self.SORT_ID:int = sortId
	
	def __json__(self) -> dict[str, str | None | int]:
		return {
			"id": self.ID,
			"name": self.NAME,
			"sort_id": self.SORT_ID
		}
	
	def __str__(self) -> str:
		return str(self.__json__())

class Enhancement:
	def __init__(self, level:int, ingredients:list[item.Ingredient], name:str, category:int) -> None:
		self.LEVEL:int = level
		self.INGREDIENTS:list[item.Ingredient] = ingredients
		self.NAME:str = name
		self.CATEGORY:int = category  
	
	def __json__(self) -> dict[str, str | int | list[dict[str, str | int]]]:
		return {
			"level": self.LEVEL,
			"ingredients": [i.__json__() for i in self.INGREDIENTS],
			"name": self.NAME,
			"category": self.CATEGORY
		}
	
	def __str__(self) -> str:
		return str(self.__json__())

class SkillLevel(Enhancement):
	def __init__(self, level: int, ingredients: list[item.Ingredient], name: str, category: int) -> None:
		super().__init__(level, ingredients, name, category)

class SkillMastery(Enhancement):
	def __init__(self, level: int, ingredients: list[item.Ingredient], name: str, category: int) -> None:
		super().__init__(level, ingredients, name, category)

class Skill:
	def __init__(self, id:str, iconId:str|None, name:str, masteries:list[SkillMastery]) -> None:
		self.ID:str = id
		self.ICON_ID:str | None = iconId
		self.NAME:str = name
		self.MASTERIES:list[SkillMastery] = masteries
	
	def __json__(self) -> dict[str, str | None | list[dict[str, str | int | list[dict[str, str | int]]]]]:
		return {
			"id": self.ID,
			"icon_id": self.ICON_ID,
			"name": self.NAME,
			"stages": [m.__json__() for m in self.MASTERIES]
		}
	
	def __str__(self) -> str:
		return str(self.__json__())
	
class ModuleStage(Enhancement):
	def __init__(self, level: int, ingredients: list[item.Ingredient], name: str, category: int) -> None:
		super().__init__(level, ingredients, name, category)

class Module:
	def __init__(self, name:str, id:str, typeName:str, stages:list[ModuleStage], isCnOnly:bool) -> None:
		self.NAME:str = name
		self.ID:str = id
		self.TYPE_NAME:str = typeName
		self.STAGES:list[ModuleStage] = stages
		self.IS_CN_ONLY:bool = isCnOnly
	
	def __json__(self) -> dict[str, str | bool | list[dict[str, str | int | list[dict[str, str | int]]]]]:
		return {
			"name": self.NAME,
			"id": self.ID,
			"type_name": self.TYPE_NAME,
			"stages": [s.__json__() for s in self.STAGES],
			"is_cn_only": self.IS_CN_ONLY
		}
	
	def __str__(self) -> str:
		return str(self.__json__())

class Potential:
	def __init__(self, name:str) -> None:
		self.NAME:str = name
	
	def __json__(self) -> dict[str, str]:
		return {
			"name": self.NAME
		}
	
	def __str__(self) -> str:
		return str(self.__json__())

class Promotion(Enhancement):
	def __init__(self, level: int, ingredients: list[item.Ingredient], name: str, category: int) -> None:
		super().__init__(level, ingredients, name, category)

class Operator:
	def __init__(self, id:str, name:str, cnName:str, rarity:int, className:str, isCnOnly:bool, skills:list[Skill], modules:list[Module], potentials:list[Potential], promotions:list[Promotion]) -> None:
		self.ID:str = id
		self.NAME:str = name
		self.CN_NAME:str = cnName
		self.RARITY:int = rarity
		self.CLASS:str = className
		self.IS_CN_ONLY:bool = isCnOnly
		self.SKILLS:list[Skill] = skills
		self.MODULES:list[Module] = modules #
		self.POTENTIALS:list[Potential] = potentials
		self.PROMOTIONS:list[Promotion] = promotions
		self.level:int
	
	def __json__(self) -> dict[str, str | int | bool | list[dict[str, str | None | list[dict[str, str | int | list[dict[str, str | int]]]]]] | list[dict[str, str | bool | list[dict[str, str | int | list[dict[str, str | int]]]]]] | list[dict[str, str]] | list[dict[str, str | int | list[dict[str, str | int]]]]]:
		return {
			"id": self.ID,
			"name": self.NAME,
			"cn_name": self.CN_NAME,
			"rarity": self.RARITY,
			"class": self.CLASS,
			"is_cn_only": self.IS_CN_ONLY,
			"skills": [s.__json__() for s in self.SKILLS],
			"modules": [m.__json__() for m in self.MODULES],
			"potentials": [p.__json__() for p in self.POTENTIALS],
			"promotions": [p.__json__() for p in self.PROMOTIONS]
		}

	def __str__(self) -> str:
		return str(self.__json__())

def operatorsFromJson() -> list[Operator]:
    return [json.load(open(OPERATOR_FILE))];