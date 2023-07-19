import io, os, re, sys
import datetime

from abs import stringify

from Store import Store
from fetch import fetch


URL = "https://www.ibtimes.com"


@stringify
class ArticleBlock:
	REGEX = re.compile(r'<article>\s*(.+?)\s*</article>', re.S)

	@classmethod
	def iter(cls, text):
		for m in cls.REGEX.finditer(text):
			yield m.group(1)


class ArticleItem:
	REGEX = re.compile(r'(href|src|alt)="(.+?)"|<div class="summary">(.+?)</div>|<h3.*?>(.+?)</h3>', re.S)

	def __init__(self, key, val):
		self.key = key
		self.val = val

	@classmethod
	def iter(cls, text):
		for x in cls.REGEX.finditer(text):
			if x.group(1):
				yield ArticleItem(x.group(1), x.group(2))
			elif x.group(3):
				yield ArticleItem("summary", x.group(3))
			elif x.group(4):
				yield ArticleItem("h3", x.group(4))


@stringify
class Headline:
	def __init__(self):
		self.href = ""
		self.src = ""
		self.alt = ""
		self.h3 = ""
		self.summary = ""

	@property
	def title(self):
		return Title.parse(self.h3)

	@classmethod
	def from_article_items(cls, items):
		obj = cls()
		for item in items:
			#~ print("%10s |" % k.upper(), v)
			if item.key == "href" and not obj.href: obj.href = normalize_link(item.val)
			elif item.key == "src" and not obj.src: obj.src = item.val
			elif item.key == "alt" and not obj.alt: obj.alt = item.val
			elif item.key == "h3" and not obj.h3: obj.h3 = item.val
			elif item.key == "summary" and not obj.summary: obj.summary = item.val
		return obj


@stringify
class Title:
	REGEX = re.compile(r'\s*(?:<div.*?</div>.*?)?<a (href|data-vid)="(.+?)".*?>\s*(.+?)\s*<', re.S)

	def __init__(self, type="", link="", text=""):
		self.type = type
		self.link = link
		self.text = text

	@classmethod
	def parse(cls, text):
		#~ print(text)
		m = cls.REGEX.search(text)
		if not m: return None
		return Title(m.group(1), normalize_link(m.group(2)), m.group(3))


def genrss(text, file=sys.stdout):
	dt = datetime.datetime.now(datetime.timezone.utc)

	file.write('<rss version="0.91">\n\t<channel>\n')
	file.write('\t\t<title>IBT</title>\n')
	file.write(f'\t\t<link>{URL}</link>\n')
	file.write('\t\t<description>RSS Feed of the International Business Times</description>\n')
	file.write('\t\t<language>en-us</language>\n')
	file.write('\t\t<copyright>Copyright 2023 IBTimes LLC. All Rights Reserved</copyright>\n')
	file.write(f'\t\t<lastBuildDate>{dt:%a, %d %b %Y %H:%M} GMT</lastBuildDate>\n')
	file.write('\t\t<skipHours>1</skipHours>\n')
	file.write('\t\t<managingEditor>https://github.com/dejbug</managingEditor>\n')
	file.write('\t\t<webMaster>https://github.com/dejbug</webMaster>\n')
	for block in ArticleBlock.iter(text):
		headline = Headline.from_article_items(ArticleItem.iter(block))
		file.write('\t\t\t<item>\n')
		title = headline.title
		file.write(f'\t\t\t\t<title>{title.text}</title>\n')
		if title.type == "href":
			file.write(f'\t\t\t\t<link>{title.link}</link>\n')
		if headline.summary:
			file.write(f'\t\t\t\t<description>{headline.summary}</description>\n')
		file.write('\t\t\t</item>\n')
	file.write('\t</channel>\n</rss>\n')


def genatom(text, file=sys.stdout):
	dt = datetime.datetime.now(datetime.timezone.utc)
	updated = f'<updated>{dt:%Y-%m-%dT%H:%M:%S}Z</updated>'

	file.write('<?xml version="1.0" encoding="utf-8"?>\n')
	file.write('\t<feed xmlns="http://www.w3.org/2005/Atom">\n')
	file.write('\t\t<title>IBT</title>\n')
	file.write(f'\t\t<link href="{URL}"/>\n')
	file.write(f'\t\t{updated}\n')
	file.write('\t\t<author>\n')
	#~ file.write('\t\t\t<name>Dejan Budimir</name>\n')
	#~ file.write('\t\t\t<uri>https://github.com/dejbug</uri>\n')
	file.write('\t\t\t<name>International Business Times</name>\n')
	file.write(f'\t\t\t<uri>{URL}</uri>\n')
	file.write('\t\t</author>\n')
	file.write(f'\t\t<rights>Copyright 2023 IBTimes LLC. All Rights Reserved</rights>\n')
	file.write(f'\t\t<id>{URL}</id>\n')
	for block in ArticleBlock.iter(text):
		headline = Headline.from_article_items(ArticleItem.iter(block))
		file.write('\t\t\t<entry>\n')
		title = headline.title
		file.write(f'\t\t\t\t<title>{title.text}</title>\n')
		if title.type == "href":
			file.write(f'\t\t\t\t<link href="{title.link}"/>\n')
			file.write(f'\t\t\t\t<id>{title.link}</id>\n')
		if headline.summary:
			file.write(f'\t\t\t\t<summary>{headline.summary}</summary>\n')
		file.write(f'\t\t\t\t{updated}\n')
		#~ file.write('\t\t\t\t<author>\n')
		#~ file.write('\t\t\t\t\t<name>International Business Times</name>\n')
		#~ file.write(f'\t\t\t\t\t<uri>{URL}</uri>\n')
		#~ file.write('\t\t\t\t</author>\n')
		file.write('\t\t\t</entry>\n')
	file.write('\t</feed>\n')


def normalize_link(text):
	return "https://www.ibtimes.com" + text if text.startswith("/") else text


def parse(text):
	buffer = io.StringIO()
	genatom(text, buffer)
	return buffer.getvalue()


def load():
	store = Store(URL)
	# print(store.age)

	if store.expired:
		text = fetch(URL)
		store.text = text
		atom = parse(text)
		store.atom = atom
		return atom

	return store.atom


def main_native():
	atom = load()
	print(atom)


def main_spinned(request):
	#~ print(dir(request), request.method, request.headers)
	#~ route = request.headers["spin-component-route"].strip("/")
	#~ print(route)

	#~ rate = int(os.environ["RATE"])
	#~ print(rate)

	atom = load()
	return Response(200, {"content-type": "text/xml"}, bytes(atom, "utf-8"))
	#~ return Response(200, {"content-type": "text/plain"}, bytes("No such feed.", "utf-8"))


try:
	from spin_http import Response
except:
	handle_request = main_native
else:
	handle_request = main_spinned


if __name__ == "__main__":
	sys.exit(handle_request())

