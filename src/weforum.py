import sys, re, json, io, datetime, collections

from lib.utils import xml_escape

class Error(Exception): pass
class ParseError(Error): pass

VERSION = "0.4.0"


URL = "https://www.weforum.org/agenda/feed"

TITLE = "World Economic Forum"
TITLE_SHORT = "weforum.org"
COPYRIGHT = "Copyright 2023 World Economic Forum"

HEADERS = {}


Source = collections.namedtuple("Source", "id name")
Topic = collections.namedtuple("Topic", "id title url")
Author = collections.namedtuple("Author", "id name")
Article = collections.namedtuple("Article", "id url title description ocap ecap sref tref arefs")
Ref = collections.namedtuple("Ref", "id")


def extract_json(text):
	m = re.search("window\.__APOLLO_STATE__\['.*?']=(\{\"Topic:.+?}]}}});", text, re.S)
	if m:
		try:
			return json.loads(m.group(1))
		except json.decoder.JSONDecodeError:
			pass


def json_get(data, *aa):
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


def normalize_name(text):
	return re.sub(r'[ \t]+', ' ', text).strip()


# def merge_descriptions(article):
# 	s = ""
# 	if article.ecap: s += article.ecap
# 	if article.description: s += " / " + article.description
# 	return s


def print_article_as_atom(article, file=sys.stdout):
	file.write('<entry>\n')
	file.write(f'\t<category term="{article.tref.url}" label="{article.tref.title}"/>\n')
	file.write(f'\t<title>{xml_escape(article.title)}</title>\n')
	file.write(f'\t<link href="{article.url}"/>\n')
	file.write(f'\t<id>{article.url}</id>\n')
	for author in article.arefs:
		file.write('\t<contributor>\n')
		file.write(f'\t\t<name>{normalize_name(author.name)}</name>\n')
		file.write('\t</contributor>\n')
	if article.ecap:
		file.write(f'\t<summary>{article.ecap}</summary>\n')
	if article.description:
		file.write(f'\t<content{article.description}</content>\n')
	file.write('</entry>\n')


def genatom(articles, file=sys.stdout):
	dt = datetime.datetime.now(datetime.timezone.utc)
	updated = f'<updated>{dt:%Y-%m-%dT%H:%M:%S}Z</updated>'

	file.write('<?xml version="1.0" encoding="utf-8"?>\n')
	file.write('<feed xmlns="http://www.w3.org/2005/Atom">\n')
	file.write(f'\t<title>{TITLE}</title>\n')
	file.write(f'\t<link href="{URL}"/>\n')
	file.write(f'\t{updated}\n')
	file.write('\t<author>\n')
	file.write(f'\t\t<name>{TITLE_SHORT}</name>\n')
	file.write(f'\t\t<uri>{URL}</uri>\n')
	file.write('\t</author>\n')
	file.write(f'\t<rights>{COPYRIGHT}</rights>\n')
	file.write(f'\t<id>{URL}</id>\n')
	file.write(f'\t<generator uri="https://atoms.fermyon.app" version="{VERSION}">\n')
	file.write(f'\t\tWhere is my complimentary Fermyon T-Shirt? -- Dejan\n')
	file.write(f'\t</generator>\n')
	for article in articles:
		print_article_as_atom(article, file=file)
	file.write('</feed>')


def parse_ref(text):
	if text:
		return text.split(':')[1]


def parse_author_refs(texts):
	if texts:
		aa = []
		for text in texts:
			aa.append(parse_ref(text))
		return aa


def parse_items(text):
	data = extract_json(text)
	if data:
		for key, item in data.items():
			t = item['__typename']
			if t == 'Topic':
				yield Topic(item['id'], item['title'], item['url'])
			elif t == 'Author':
				yield Author(item['id'], item['name'])
			elif t == 'Article':
				ocap = json_get(item, 'featuredImage', 'table', 'original_caption')
				ecap = json_get(item, 'featuredImage', 'table', 'edited_caption')
				sref = parse_ref(json_get(item, 'source', '__ref'))
				tref = parse_ref(json_get(item, 'topic', '__ref'))
				arefs = parse_author_refs(json_get(item, 'authors', '__ref'))
				yield Article(item['id'], item['url'], item['title'],
					item['description'], ocap, ecap, sref, tref, arefs)
			elif t == 'Source':
				yield Source(item['id'], item['name'])
			elif t == 'Query': continue
			else:
				# import pprint
				# pprint.pprint(item)
				print(item)
				raise ParseError(f'unknown item type {t}')


def parse_articles(text):
	sources = {}
	topics = {}
	authors = {}

	for item in parse_items(text):
		if isinstance(item, Source):
			sources[item.id] = item
		elif isinstance(item, Topic):
			topics[item.id] = item
		elif isinstance(item, Author):
			authors[item.id] = item
		elif isinstance(item, Article):
			item = resolve_article_refs(item, sources, topics, authors)
			yield item
		# print(item)
		# print()


def parse(text):
	buffer = io.StringIO()
	genatom(parse_articles(text), buffer)
	return buffer.getvalue()


def resolve_article_refs(article, sources, topics, authors):
	id, url, title, description, ocap, ecap, sref, tref, arefs = article

	_arefs = []

	if sref:
		if sref in sources:
			# print('RESOLVED', sources[sref])
			sref = sources[sref]
	if tref:
		if tref in topics:
			# print('RESOLVED', topics[tref])
			tref = topics[tref]
	if arefs:
		for aref in arefs:
			if aref in authors:
				# print('RESOLVED', authors[aref])
				_arefs.append(authors[aref])

	return Article(id, url, title, description, ocap, ecap,
		sref, tref, _arefs)


if __name__ == '__main__':

	if 0:
		data = {
			'1':{
				'1.1':{
					'1.1.1':{},
					'1.1.2':{},
				},
				'1.2':{
					'1.2.1':{},
					'1.2.2':{
						'x':[
							{'blah': 'a'},
							{'blah': 'b'},
							{'blah': 'c'},
						]
					},
				}
			}
		}
		print(json_get(data, '1', '1.2', '1.2.2', 'x', 'blah'))
		exit()

	if 0:
		with open('.cache/weforum.text') as file:
			for item in parse_articles(file.read()):
				print(item)
				print()

	if 1:
		with open('.cache/weforum.text') as file:
			print(parse(file.read()))
