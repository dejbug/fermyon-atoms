import re, json, pprint


def extractJson(text):
	m = re.search("window\.__APOLLO_STATE__\['.*?']=(\{\"Topic:.+?}]}}});", text, re.S)
	o = json.loads(m.group(1))
	return o


def iterObjects(text):
	return (findObjectEnd(text, m.start(0)) for m in re.finditer(r'\{"id":"', text, re.S))


def findObjectEnd(text, start):
	assert text[start] == '{'
	length = 1
	nesting = 1
	for c in text[start + 1:]:
		if c == '{': nesting += 1
		elif c == '}': nesting -= 1
		if nesting <= 0: break
		length += 1
	return text[start:start+length]


def parseObject(text):
	return (m.groups() for m in re.finditer(r'"(.+?)":"(.+?)"', text, re.S))



if __name__ == "__main__":
	with open('.cache/weforum.text') as file:
		text = file.read()

	# data = extractJson(text)
	# pprint.pprint(data)

	for block in iterObjects(text):
		for key, val in parseObject(block):
			print(key, val)
		print()
