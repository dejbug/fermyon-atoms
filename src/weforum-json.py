import sys, re, json, io, datetime, collections

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from grammars.weforum.weforumLexer import weforumLexer
from grammars.weforum.weforumParser import weforumParser
from grammars.weforum.weforumListener import weforumListener

# We have to do this otherwise we get a strange error:
#	OSError: [Errno 8] Bad file descriptor: '/1/antlr4'
# See: antlr4.ErrorStrategy.sync
# See: antlr4.atn.ATN.nextTokensInContext
# This might be a Python version issue.
from antlr4 import LL1Analyzer

from lib.utils import xml_escape


URL = "https://www.weforum.org/agenda/feed"

TITLE = "World Economic Forum"
TITLE_SHORT = "weforum.org"
COPYRIGHT = "Copyright 2023 World Economic Forum"

HEADERS = {}


def extract_json(text):
	m = re.search("window\.__APOLLO_STATE__\['.*?']=(\{\"Topic:.+?}]}}});", text, re.S)
	if m:
		try:
			return json.loads(m.group(1))
		except json.decoder.JSONDecodeError:
			pass


Topic = collections.namedtuple("Topic", "id title url")
Author = collections.namedtuple("Author", "id name")
Article = collections.namedtuple("Article", "id url title")
Ref = collections.namedtuple("Ref", "id")


def normalize_name(text):
	return re.sub(r'[ \t]+', ' ', text)


def parse_topic(topic):
	if not topic: return topic
	m = re.search(r'"id":"(\d+)".*?,"title":"(.+?)","url":"(.+?)"', topic.getText(), re.S)
	if m: return Topic(*m.groups())

def parse_authors(authors):
	if not authors: return authors
	for author in authors:
		yield parse_author(author)

def parse_author(author):
	if not author: return author
	m = re.search(r'"id":"(\d+)".*?,"name":"(.+?)"', author.getText(), re.S)
	if m: return Author(m.group(1), normalize_name(m.group(2)))

def parse_article(article):
	if not article: return article
	m = re.search(r'"id":"(\d+)".*?,"url":"(.+?)","title":"(.+?)"', article.getText(), re.S)
	if m: return Article(*m.groups())

def parse_authorsRef(authorsRef):
	if not authorsRef: []
	for ref in authorsRef:
		for x in re.finditer(r'"Author:(\d+)"', ref.getText(), re.S):
			yield Ref(*x.groups())

def parse_topicRef(topicRef):
	if not topicRef: return []
	for ref in topicRef:
		for x in re.finditer(r'"Topic:(\d+)"', ref.getText(), re.S):
			return Ref(*x.groups())


def parse_item(ctx, resolver, debug = True):
	topic = parse_topic(ctx.Topic())
	resolver.add_topic(topic)
	if debug: print("TOPIC", topic, "\n")

	authors = list(parse_authors(ctx.Author()))
	resolver.add_authors(authors)
	if debug: print("AUTHORS", authors, "\n")

	article = parse_article(ctx.Article())
	if debug: print("ARTICLE", article, "\n")

	authorsRef = list(parse_authorsRef(ctx.AuthorsRef()))
	if debug: print("AUTHORS REF", authorsRef)
	if debug: print("AUTHORS DEREF", authorsRef, list(resolver.deref_authors(authorsRef)), "\n")
	# authors = resolver.resolve_authors(authors, authorsRef)
	# if debug: print("AUTHORS RESOLVED", authors, "\n")

	topicRef = parse_topicRef(ctx.TopicRef())
	if debug: print("TOPIC REF", topicRef)
	if debug: print("TOPIC DEREF", topicRef, resolver.deref_topic(topicRef), "\n")
	# topic = resolver.resolve_topic(topic, topicRef)
	# if debug: print("TOPIC RESOLVED", topic, "\n")

	if debug: print_item((topic, authors, article))

	if debug: print("-" * 79)
	return (topic, authors, article, authorsRef, topicRef)


def print_item(item):
	topic, authors, article = item
	print(topic.title if topic else "[NO TOPIC]")
	print(article.title)
	print(article.url)
	for author in authors:
		print(author.name)
	print()


def print_item_as_atom(item, file=sys.stdout):
	topic, authors, article = item
	file.write('<entry>\n')
	file.write(f'\t<category term="{topic.url}" label="{topic.title}"/>\n')
	file.write(f'\t<title>{xml_escape(article.title)}</title>\n')
	file.write(f'\t<link href="{article.url}"/>\n')
	file.write(f'\t<id>{article.url}</id>\n')
	for author in authors:
		file.write('\t<contributor>\n')
		file.write(f'\t\t<name>{author.name}</name>\n')
		file.write('\t</contributor>\n')
	file.write('</entry>\n')


class Merger:
	def __init__(self, key):
		self.key = key
		self.mapping = {}

	def add(self, items):
		for item in items:
			self.mapping[getattr(item, self.key)] = item

	def get(self):
		return self.mapping.values()


class Resolver:
	def __init__(self):
		self.authors = []
		self.topics = []

	def add_author(self, author):
		self.authors.append(author)

	def add_authors(self, authors):
		for author in authors:
			if author:
				self.add_author(author)

	def add_topic(self, topic):
		if topic:
			self.topics.append(topic)

	def deref_author(self, ref):
		for author in self.authors:
			if author.id == ref.id:
				return author

	def deref_authors(self, refs):
		for ref in refs:
			yield self.deref_author(ref)

	def deref_topic(self, ref):
		for topic in self.topics:
			if topic.id == ref.id:
				return topic

	def resolve_authors(self, authors, refs):
		merger = Merger("name")
		merger.add(authors)
		resolved = list(self.deref_author(ref) for ref in refs)
		print(authors, refs, resolved)
		merger.add(resolved)
		return merger.get()

	def resolve_topic(self, topic, ref):
		if topic:
			if ref:
				assert topic.id == ref.id
			return topic
		elif ref:
			return self.deref_topic(ref)


class Listener(weforumListener):
	def __init__(self):
		self.items = []
		self.resolver = Resolver()

	def resolve_all(self, debug = True):
		for item in self.items:
			topic, authors, article, authorsRef, topicRef = item

			authors = self.resolver.resolve_authors(authors, authorsRef)
			if debug: print("AUTHORS RESOLVED", authors, "\n")

			topic = self.resolver.resolve_topic(topic, topicRef)
			if debug: print("TOPIC RESOLVED", topic, "\n")

	def exitArticle(self, ctx):
		# print(type(ctx))
		# print(dir(ctx))
		# print(ctx.toStringTree())
		# print(ctx.children)
		self.items.append(parse_item(ctx, self.resolver))


def genatom(items, file=sys.stdout):
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
	for item in items:
		print_item_as_atom(item, file=file)
	file.write('</feed>')


def parse_items(text):
	input = InputStream(text)
	lexer = weforumLexer(input)
	stream = CommonTokenStream(lexer)
	parser = weforumParser(stream)
	tree = parser.start()
	# print(tree.toStringTree(recog=parser))

	listener = Listener()
	walker = ParseTreeWalker()
	walker.walk(listener, tree)

	listener.resolve_all()

	return listener.items


def parse(text):
	# input = InputStream(text)
	# lexer = weforumLexer(input)
	# stream = CommonTokenStream(lexer)
	# parser = weforumParser(stream)
	# tree = parser.start()
	# print(tree.toStringTree(recog=parser))

	# listener = Listener()
	# walker = ParseTreeWalker()
	# walker.walk(listener, tree)

	buffer = io.StringIO()
	# genatom(listener.items, buffer)
	genatom(parse_items(text), buffer)
	return buffer.getvalue()


def parse_json(text):
	import pprint
	data = extract_json(text)
	# print(data.keys())
	for key, item in data.items():
		t = item['__typename']
		if t == 'Topic':
			print(t.upper(), item['id'], item['title'], item['url'],)
			print()
		elif t == 'Author':
			print(t.upper(), item['id'], item['name'])
			print()
		elif t == 'Article':
			print(t.upper(), item['id'], item['title'], item['url'])
			print()
			print('Description', item['description'])
			print()
			print('Caption-O', item['featuredImage']['table']['original_caption'])
			print('Caption-E', item['featuredImage']['table']['edited_caption'])
			print()
		elif t == 'Source':
			print(t.upper(), item['id'], item['name'])
			print()
		elif t == 'Query': continue
		else:
			pprint.pprint(item)
			break


if __name__ == '__main__':
	with open('.cache/weforum.text') as file:
		text = file.read()

	# print(parse(text))

	# for item in parse_items(text):
		# print(item)

	# parse_items(text)

	import pprint
	data = extract_json(text)
	# print(data.keys())
	for key, item in data.items():
		t = item['__typename']
		if t == 'Topic':
			print(t.upper(), item['id'], item['title'], item['url'],)
			print()
		elif t == 'Author':
			print(t.upper(), item['id'], item['name'])
			print()
		elif t == 'Article':
			print(t.upper(), item['id'], item['title'], item['url'])
			print()
			print('Description', item['description'])
			print()
			print('Caption-O', item['featuredImage']['table']['original_caption'])
			print('Caption-E', item['featuredImage']['table']['edited_caption'])
			print()
		elif t == 'Source':
			print(t.upper(), item['id'], item['name'])
			print()
		elif t == 'Query': continue
		else:
			pprint.pprint(item)
			break

