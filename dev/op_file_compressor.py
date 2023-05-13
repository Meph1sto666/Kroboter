import json
data:dict[str, dict[str, list[dict[str, None]]]] = json.load(open('../operators_uncompressed.json', encoding="utf-8"))
for d in data:
	try: 
		for s in range(len(data[d]["skills"])):
			try: data[d]["skills"][s].pop("masteries")
			except: pass
			try:
				if data[d]["skills"][s]["iconId"] == None: data[d]["skills"][s].pop("iconId")
			except: pass
	except: pass
	try: 
		if len(data[d]["skills"]) <= 0: data[d].pop("skills")
	except: pass
	try:
		if len(data[d]["modules"]) <= 0: data[d].pop("modules")
	except: pass
	try:
		data[d].pop("elite")
	except: pass
	try:
		if not data[d]["isCnOnly"]: data[d].pop("isCnOnly")
	except: pass
	data[d].pop("skillLevels")
	try:
		for s in range(len(data[d]["elite"])):
			try: data[d]["elite"][s].pop("ingredients")
			except: pass
	except: pass
	try:
		for s in range(len(data[d]["modules"])):
			if not data[d]["modules"][s]["isCnOnly"]: data[d]["modules"][s].pop("isCnOnly")
			# try: data[d]["modules"][s].pop("isCnOnly")
			# except: pass
			try: data[d]["modules"][s].pop("stages")
			except: pass
	except: pass
print(data["char_474_glady"])
json.dump(data, open("./data/operators.json", "w", encoding="utf-8"), indent=4)