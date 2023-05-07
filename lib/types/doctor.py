from datetime import datetime as dt
from lib.types.operator import *


class Profile:
	def __init__(self, display_name: str, friend_code: str, level: int | None, server: str | None, onboard: str | None, assistant: str | None, supports: list[dict[str, str | int | None | list[int]]] | None) -> None:
		self.name: str = display_name
		self.code: str = friend_code
		self.level: int = level if level != None else 0
		self.server: str | None = server
		self.onboard: dt | None = dt.fromisoformat(onboard) if onboard != None else None
		self.assistant: str | None = assistant
		self.supports: list[Operator] = [Operator(**s) for s in supports] if supports != None else [] # type: ignore