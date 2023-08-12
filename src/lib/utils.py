import re, html


def collapse_whitespace(text):
	return re.sub(r'[ \t]+', ' ', text).strip()


def xml_escape(text):
	text = html.unescape(text)
	text = re.sub(r'&', '&amp;', text, re.S)
	text = re.sub(r'<', '&lt;', text, re.S)
	text = re.sub(r'>', '&gt;', text, re.S)
	text = re.sub(r'\'', '&apos;', text, re.S)
	text = re.sub(r'"', '&quot;', text, re.S)
	return text


def json_get(data, *aa):
	'''
	>>> data = {
	... 	'1': {
	... 		'1.1': {
	... 			'1.1.1': {},
	... 			'1.1.2': {},
	... 		},
	... 		'1.2': {
	... 			'1.2.1': {},
	... 			'1.2.2': {
	... 				'list': [
	... 					{'item': 'a'},
	... 					{'item': 'b'},
	... 					{'item': 'c'},
	... 				]
	... 			},
	... 		}
	... 	}
	... }
	>>> json_get(data, '1', '1.2')
	{'1.2.1': {}, '1.2.2': {'list': [{'item': 'a'}, {'item': 'b'}, {'item': 'c'}]}}
	>>> json_get(data, '1', '1.2', '1.2.2', 'XXXX', 'item')
	>>> json_get(data, '1', '1.2', '1.2.2', 'list', 'item')
	['a', 'b', 'c']
	>>> json_get(data, '1', '1.2', '1.2.2', 'list', 'XXXX')
	[None, None, None]
	>>> json_get(data, '1', '1.3', '1.2.2', 'list', 'XXXX')
	'''
	for i, a in enumerate(aa):
		if not data:
			return None
		elif isinstance(data, list):
			return [json_get(item, *aa[i:]) for item in data]
		elif a not in data:
			return None
		else:
			data = data[a]
	# return data
	return data.strip() if isinstance(data, str) else data


def get_version_from_manifest():
	with open('spin.toml') as file:
		m = re.search(r'^version\s*=\s*"(.+?)"', file.read(), re.M)
		if not m: return ""
		return m.group(1)
