import sys, re, collections, datetime
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from grammars.weforum.weforumLexer import weforumLexer
from grammars.weforum.weforumParser import weforumParser
from grammars.weforum.weforumParserListener import weforumParserListener


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
	if not authorsRef: return authorsRef
	for x in re.finditer(r'"Author:(\d+)"', authorsRef.getText(), re.S):
		yield Ref(*x.groups())

def parse_topicRef(topicRef):
	if not topicRef: return topicRef
	for x in re.finditer(r'"Topic:(\d+)"', topicRef.getText(), re.S):
		return Ref(*x.groups())


def parse_item(ctx, resolver):
	topic = parse_topic(ctx.Topic())
	resolver.add_topic(topic)
	# print("TOPIC", topic, "\n")

	authors = list(parse_authors(ctx.Author()))
	resolver.add_authors(authors)
	# print("AUTHORS", authors, "\n")

	article = parse_article(ctx.Article())
	# print("ARTICLE", article, "\n")

	authorsRef = list(parse_authorsRef(ctx.AuthorsRef()))
	# print("AUTHORS REF", authorsRef, list(resolver.deref_authors(authorsRef)), "\n")
	authors = resolver.resolve_authors(authors, authorsRef)
	# print("AUTHORS RESOLVED", authors, "\n")

	topicRef = parse_topicRef(ctx.TopicRef())
	# print("TOPIC REF", topicRef, resolver.deref_topic(topicRef), "\n")
	topic = resolver.resolve_topic(topic, topicRef)
	# print("TOPIC RESOLVED", topic, "\n")

	# print()
	# print_item((topic, authors, article))

	# print("-" * 79)
	return (topic, authors, article)


def print_item(item):
	topic, authors, article = item
	print(topic.title)
	print(article.title)
	print(article.url)
	for author in authors:
		print(author.name)
	print()


def print_item_as_atom(item, file=sys.stdout):
	topic, authors, article = item
	file.write('<entry>\n')
	file.write(f'\t<category term="{topic.url}" label="{topic.title}"/>\n')
	file.write(f'\t<title>{article.title}</title>\n')
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
		merger.add(resolved)
		return merger.get()

	def resolve_topic(self, topic, ref):
		if topic:
			if ref:
				assert topic.id == ref.id
			return topic
		elif ref:
			return self.deref_topic(ref)


class Listener(weforumParserListener):
	def __init__(self):
		self.items = []
		self.resolver = Resolver()

	def exitArticle(self, ctx):
		# print(dir(ctx))
		# print(ctx.toStringTree())
		# print(ctx.children)
		self.items.append(parse_item(ctx, self.resolver))


def parse(path, encoding="utf-8"):
	input = FileStream(path, encoding=encoding)
	lexer = weforumLexer(input)
	stream = CommonTokenStream(lexer)
	parser = weforumParser(stream)
	tree = parser.r()
	# print(tree.toStringTree(recog=parser))
	listener = Listener()
	walker = ParseTreeWalker()
	walker.walk(listener, tree)
	return listener.items


def print_feed(items, file=sys.stdout):
	dt = datetime.datetime.now(datetime.timezone.utc)
	updated = f'<updated>{dt:%Y-%m-%dT%H:%M:%S}Z</updated>'

	URL = "https://www.weforum.org/agenda/feed"

	TITLE = "World Economic Forum"
	TITLE_SHORT = "weforum"
	COPYRIGHT = "Copyright 2023 World Economic Forum"

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
	file.write('</feed>\n')


def main(argv):
	items = parse(argv[1])
	# for item in items:
		# print_item(item)
		# print_item_as_atom(item)
	print_feed(items)


if __name__ == '__main__':
	sys.exit(main(sys.argv))
