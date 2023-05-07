x=0
y=0
def hash(t:str) -> int:
	hash:int=0
	for c in t:
		# hash=(hash*77^ord(c)*1)&0xFFFFFFFF
		# hash=(hash*179^ord(c)*236)&0xFFFFFFFF
		hash=(hash*235^ord(c)+651)&0xFFFFFFFF
	return hash

def textToColor(t:str) -> tuple[int,int,int]:
	return ((hash(t)&0xFF0000)>>16,(hash(t)&0xFF00)>>8,(hash(t)&0xFF))

def rgbToHex(v:tuple[int,int,int]) -> str:
	return f"#{''.join([hex(c)[2:].rjust(2,'0') for c in v])}"

def hexToRgb(h:str) -> tuple[int, int, int]:
	if h.startswith("#"): h=h[1:]
	elif h.startswith("0x"): h=h[1:]
	return tuple(int(r, 16) for r in [h[n:n+2] for n in range(0, len(h), 2)])
