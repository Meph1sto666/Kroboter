import json
from lib.types.operator import *
data:dict[str, list[str | dict[str, str | int | list[str]]]] = json.load(open("./data/recruitment.json", "r", encoding="utf-8"))
# operators: list[operators] = data.get("ops", []) # type: ignore
operators: list[RecruitmentOp] = [RecruitmentOp(**o) for o in data.get("ops", [])] # type: ignore
tags: list[str] = data.get("tags", []) # type: ignore

a: list[str]=["DPS","Ranged","Sniper","Top Operator","Senior Operator","DP-Recovery","Melee","Vanguard","AoE","Debuff","Caster","Healing","Support","Medic","Defense","Defender","Guard","Survival","Nuker","Slow","Supporter","Crowd-Control","Specialist","Fast-Redeploy","Summon","Shift","Starter","Robot"]

sTags:list[str] = ["Fast-Redeploy", "Sniper", "AoE", "Slow", "Starter"]

res: dict[str, list[RecruitmentOp]] = {}
for o in operators:
	tagStrs: str = o.createMatchingTagsStrs(sTags,data["grouped_tags"]["rarity"]) # type: ignore
	for ts in tagStrs:
		if res.get(ts) == None: res[ts] = []
		# res[ts].append(f"```{o.name}```")
		res[ts].append(o)
for r in dict(res).keys():
	try: res.pop("")
	except: pass
# res = dict(sorted(res.items(), key=lambda x: (len(x[1]))))
# star:str = "\U00002B50"
# sR: list[list[int]] = [list(dict.fromkeys([i.rarity for i in res[r]]))for r in res]
# raritiesL: list[tuple[str, tuple[int, int]]] = [(list(res)[s],(min(sR[s]),max(sR[s]))) for s in range(len(list(res)))]
# rarities = dict(raritiesL)
# print(rarities)
# print([(f"{r} [{f'{rarities[r][0]} - {rarities[r][1]}' if (rarities[r][1]!=rarities[r][1]) else f'{rarities[r][0]}'}] {star}") for r in res])
# print(rarities)

sR: list[list[int]] = [list(dict.fromkeys([i.rarity for i in res[r]]))for r in res]
# rarities:dict[str, list[tuple[str, tuple[int, int]]]] = dict([(list(res)[s],(min(sR[s]),max(sR[s]))) for s in range(len(list(res)))])
res = dict(sorted(res.items(), key=lambda x: (0-min([o.rarity for o in x[1]]),len(x[1]))))
print(dict([(r,[o.name for o in res[r]]) for r in res]))