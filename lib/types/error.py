class InvalidRoute(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
  
class UserDoesNotExist(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class NoSupportUnitFound(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class NoUserProfile(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class SupbaseError(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
  
class ServerError(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)