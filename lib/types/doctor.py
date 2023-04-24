from lib.types import operator

class Doctor:
	def __init__(self, level:int, operators:list[operator.Operator]) -> None:
		self.level:int = level
		self.operators:list[operator.Operator] = operators