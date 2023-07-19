import io, os, re, sys
import datetime

from Store import Store
from fetch import fetch


URL = "https://www.weforum.org/agenda/feed"

TITLE = "World Economic Forum"
TITLE_SHORT = "weforum"
COPYRIGHT = "Copyright 2023 World Economic Forum"

FORCE_LOAD = False

#~ curl 'https://www.aldaily.com/alt/' --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Alt-Used: www.aldaily.com' -H 'Connection: keep-alive'-H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: none' -H 'Sec-Fetch-User: ?1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'

def parse_dayheader(text):
	if not text: return text
	try:
		dt = datetime.datetime.strptime(text, "%B %d, %Y")
		return f'{dt:%Y-%m-%dT%H:%M:%S}Z'
	except: pass
	return text


def parse_summary(text):
	if not text: return text, None, None
	title = ""
	link = ""
	m = re.search(r'\s*<strong.*?>(.+?)</strong>\s*', text, re.S)
	if m:
		text = re.sub(r'(\s*)</?strong>(\s*)', r'\1\2', text, re.S)
		title = m.group(1)
	m = re.search(r'\s*<a.+?href="(?P<link>.+?)".*?>.*?</a>\s*', text, re.S)
	if m:
		text = text[:m.start()] + text[m.end():]
		link = m.group(1)
	text = re.sub(r'([?!.])?\.+&nbsp;$', r'\1', text, re.S)
	return text, title, link


def iter_blocks(text):
	REGEX = re.compile(
		r'<div.+?"dayheader".*?>\s*(?P<dayheader>.+?)\s*</div>|'
		r'<h3.+?class="cat".*?><a.+?href="(?P<cat_href>.+?)">'
			r'\s*(?P<cat_text>.+?)\s*</a>\s*</h3>\s*<p.*?>\s*(?P<summary>.+?)\s*</p>'
		, re.S)
	dayheader = None
	for m in REGEX.finditer(text):
		d = m.groupdict()
		if d["dayheader"]:
			dayheader = parse_dayheader(d["dayheader"])
			continue
		elif dayheader:
			d["dayheader"] = dayheader
		d["summary"], d["title"], d["link"] = parse_summary(d["summary"])
		yield d


def atom(text, file=sys.stdout):
	dt = datetime.datetime.now(datetime.timezone.utc)
	updated = f'<updated>{dt:%Y-%m-%dT%H:%M:%S}Z</updated>'

	file.write('<?xml version="1.0" encoding="utf-8"?>\n')
	file.write('<feed xmlns="http://www.w3.org/2005/Atom">\n')
	file.write(f'\t<title>{TITLE}</title>\n')
	file.write(f'\t<link href="{URL}"/>\n')
	file.write(f'\t{updated}\n')
	file.write('\t<author>\n')
	#~ file.write('\t\t<name>Dejan Budimir</name>\n')
	#~ file.write('\t\t<uri>https://github.com/dejbug</uri>\n')
	file.write(f'\t\t<name>{TITLE_SHORT}</name>\n')
	file.write(f'\t\t<uri>{URL}</uri>\n')
	file.write('\t</author>\n')
	file.write(f'\t<rights>{COPYRIGHT}</rights>\n')
	file.write(f'\t<id>{URL}</id>\n')
	for block in iter_blocks(text):
		#~ print(block)
		file.write('\t\t<entry>\n')
		file.write(f'\t\t\t<title>{block["title"]}</title>\n')
		file.write(f'\t\t\t<link href="{block["link"]}"/>\n')
		file.write(f'\t\t\t<id>{block["link"]}</id>\n')
		file.write(f'\t\t\t<summary>{block["summary"]}</summary>\n')
		file.write(f'\t\t\t{block["dayheader"]}\n')
		file.write('\t\t</entry>\n')
	file.write('</feed>\n')


def parse(text):
	buffer = io.StringIO()
	atom(text, buffer)
	return buffer.getvalue()


def load(force = FORCE_LOAD):
	store = Store(URL)
	#~ print(store.age)

	if force or not store.text or store.expired:
		text = fetch(URL)
		store.text = text
		atom = parse(text)
		store.atom = atom
		return atom

	return store.atom


def re_iter(pattern, text, flags = re.S):
	for m in re.finditer(pattern, text, flags):
		yield m.groups()


def re_search(pattern, text, flags = re.S):
	m = re.search(pattern, text, flags)
	if not m: return None
	return m.groups() if len(m.groups()) > 1 else m.groups()[0]

def iter_items(text):
	if text:
		for groups in re_iter(r'"__typename":"(.+?)"((?:,".+?":".+?")*)', text):
			#~ print(groups)
			typename, text = groups
			if typename == "Topic":
				yield "TOPIC", re_search(r'"title":"(.+?)"', text)
			elif typename == "Author":
				yield "AUTHOR", re_search(r'"name":"(.+?)"', text)
			elif typename == "Article":
				title, link = re_search(r'"url":"(.+?)","title":"(.+?)"', text)
				yield "TITLE", title
				yield "LINK", link
			else: continue


class Grammar:
	def __init__(self, text):
		self.text = text

	def __str__(self):
		return self.text

#~ print(Grammar("TOPIC AUTHOR+ TITLE LINK"))
#~ exit()


def iter_articles(text):
	grammar = ["TOPIC", ("AUTHOR", "+"), "TITLE", "LINK"]
	article = {}
	state = 0
	for key, val in iter_items(text):
		print(f"{key:>6s}", val, sep="|")
		token, flags = (grammar[state], "1") if isinstance(grammar[state], str) else grammar[state]
		if key != token:
			raise Exception(f'unexpected token "{key}"')
		article[key] = val
		state = (state + 1) % len(grammar)
		if state == 0:
			yield article
			article = {}
	if article:
		yield article


def main_native():
	#~ atom = load()
	store = Store(URL)
	for article in iter_articles(store.text):
		print(article)
	exit()

	store = Store(URL)
	if store.expired:
		text = fetch(URL)
		store.text = text
	else:
		text = store.text

	for block in iter_blocks(text):
		print(block)
		print("-" * 76)


def main_spinned(request):
	atom = load()
	return Response(200, {"content-type": "text/xml"}, bytes(atom, "utf-8"))


try:
	from spin_http import Response
except:
	handle_request = main_native
else:
	handle_request = main_spinned


if __name__ == "__main__":
	sys.exit(handle_request())
