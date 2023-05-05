from datetime import datetime as dt
from lib.types.operator import *


class Profile:
	def __init__(self, display_name: str, friend_code: str, level: int | None, server: str | None, onboard: str | None, assistant: str | None, supports: list[dict[str, str | int | None]] | None) -> None:
		self.name: str = display_name
		self.code: str = friend_code
		self.level: tuple[int | None] = level,
		self.server: str | None = server
		self.onboard: dt | None = dt.fromisoformat(onboard) if onboard != None else None
		self.assistant: str | None = assistant
		self.supports: list[SupportUnit] | None = [SupportUnit(**s) for s in supports] if supports != None else None  # type: ignore

	def __json__(self) -> dict[str, str | tuple[int | None] | dt | list[SupportUnit] | None]:
		return {
			"name": self.name,
			"code": self.code,
			"level": self.level,
			"server": self.server,
			"onboard": self.onboard,
			"assistant": self.assistant,
			"supports": self.supports,
		}