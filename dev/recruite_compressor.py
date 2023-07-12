import json
data:dict[str, dict[str, list[str] | list[dict[str, str | int | list[str]]] | list[int]]] = json.load(open('./dev/recruitment_uncompressed.json', encoding="utf-8"))

opList:list[dict[str, str | list[str] | int]] = []
opC:list[dict[str, str | list[str] | int]] = []
tags:list[str] = []

for d in data:
	opList.extend(data[d]["operators"]) # type: ignore

for o in opList:
	if not o in opC:
		opC.append(o)
		tags.extend(o.get("tags")) # type: ignore

tags = list(dict.fromkeys(tags))

json.dump({
	"tags": tags,
	"ops": opC
}, open("./data/recruitment.json", "w", encoding="utf-8"), indent=None, separators=(",", ":"))