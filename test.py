import json
from lib.types.operator import *
data:dict[str, list[str | dict[str, str | int | list[str]]]] = json.load(open("./data/recruitment.json", "r", encoding="utf-8"))
# operators: list[operators] = data.get("ops", []) # type: ignore
operators: list[RecruitmentOp] = [RecruitmentOp(**o) for o in data.get("ops", [])] # type
tags: list[str] = data.get("tags", []) # type: ignore

selectedTags:list[str] = ["Guard", "Support", "Healing", "Starter"]
print([o.name for o in list(filter(lambda o: o.matchesTags(selectedTags), operators))])