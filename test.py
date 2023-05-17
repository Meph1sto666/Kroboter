import json


unitData:dict[str, list[dict[str, str]]] = dict(json.load(open("./data/operators.json"))).get("char_4043_erato", {}) # str |
for s in ["skills", "potentials", "modules"]:
	data: list[dict[str, str]] | None = unitData.get(s)
	if data == None: continue
	if s=="modules": data = list(filter(lambda x: not x.get("isCnOnly", False), data))
	if s=="potentials":
		data.insert(0, "None") # type: ignore
		data = [{"pot_id": str(p+1),"pot_val":str(data[p])} for p in range(len(data))]