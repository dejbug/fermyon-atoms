import re

URL = "https://www.linkedin.com/pulse/topics/home"

with open('.cache/linkedin.text') as file:
	for m in re.finditer(r'<h2.*?>(.+?)</h2>', file.read(), re.S):
		print(m.group(1))
	# for m in re.finditer(r'<div class="mb-1\.5 flex flex-row">', file.read(), re.S):
	# 	print(m.group(0))
