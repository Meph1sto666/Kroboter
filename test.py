from lib.misc import *

params:list[tuple[int,int]] = [(593, 744)]

for p in params:
	print(p)
	x:int=p[0];y:int=p[1]
	[print(rgbToHex(textToColor(o))) for o in [
		"Blaze",
		"Gladiia",
		"Lumen",
		"Exusiai",

		"Breeze",
		"Goldenglow",
		"Mudrock",
		"Cantabile",
		"Shirayuki",
	]]
 
# (394, 595) breeze, blaze, gladiia, lumen
# (228, 415)? breeze, blaze, gladiia, lumen / meh

# (179, 236) EXU; GLADIIA, breeze, blaze / not bad
# (249, 720) exu, gladiia, blaze, lumen / meh

# (593, 744) blaze, glad, lum, exu