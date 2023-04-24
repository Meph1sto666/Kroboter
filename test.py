from lib.types.error import *
import json

def getRoute(key:str, data:dict[str, str]={}, route:str="", routeData:dict[str, str]={}) -> str:
	if len(route) <= 0 or routeData == {}:
		routeData = json.load(open("./data/routes.json"))
		route = routeData.get(key, "~")
	if key in route: raise InvalidRoute(route)
	if not "{" in route: return route
	return getRoute(key, data, route.format(**dict(**routeData, **data)), routeData)

print(getRoute("v1_u_profile", {"username": "12345"}))