from lib.types.error import *
import json

def getRoute(key:str, data:dict[str, str]={}, s:str="", jData:dict[str, str]={}) -> str:
	if len(s) <= 0 or jData == {}:
		jData = json.load(open("./data/api.json"))
		s = jData.get(key, "~")
	if key in s: raise InvalidRoute(s)
	if not "{" in s: return s
	return getRoute(key, data, s.format(**dict(**jData, **data)), jData)