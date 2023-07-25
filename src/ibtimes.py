import io, os, re, sys
import datetime, html

from abs import stringify

from Store import Store
from fetch import fetch


URL = "https://www.ibtimes.com"

HEADERS = {}


def normalize_link(text):
	return "https://www.ibtimes.com" + text if text.startswith("/") else text

def normalize_title(text):
	return html.escape(text)


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
		return Title(m.group(1), normalize_link(m.group(2)), normalize_title(m.group(3)))


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


def parse(text):
	buffer = io.StringIO()
	genatom(text, buffer)
	return buffer.getvalue()
