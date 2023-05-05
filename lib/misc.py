x=0
y=0
def hash(t:str) -> int:
	hash:int=0
	for c in t:
		# hash=(hash*len(t)^ord(c)*len(t))&0xFFFFFFFF
		# hash=(hash*77^ord(c)*1)&0xFFFFFFFF
		hash=(hash*179^ord(c)*236)&0xFFFFFFFF
	return hash

def textToColor(t:str) -> tuple[int,int,int]:
	return ((hash(t)&0xFF0000)>>16,(hash(t)&0xFF00)>>8,(hash(t)&0xFF))

def rgbToHex(v:tuple[int,int,int]) -> str:
	return f"#{''.join([hex(c)[2:].rjust(2,'0') for c in v])}"