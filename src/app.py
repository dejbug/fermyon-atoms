import sys, os, re, argparse

import aldaily
import ibtimes
import weforum
parsers = [ aldaily, ibtimes, weforum ]

from lib.fetch import fetch
from lib.Store import Store, LOCAL_STORE_ROOT


OFFLINE = False
REPARSE = False
REFETCH = False


try:
	from spin_http import Response

except:
	def route_from_arg(request = None):
		parser = argparse.ArgumentParser()
		parser.add_argument("-f", "--refetch", action="store_true", help="force refetch of latest site contents")
		parser.add_argument("-p", "--reparse", action="store_true", help="force reparse of old site contents")
		parser.add_argument("-o", "--offline", action="store_true", help="force working on old contents")
		parser.add_argument("route")
		args = parser.parse_args(sys.argv[1:])
		global OFFLINE, REPARSE, REFETCH
		OFFLINE = args.offline
		REPARSE = args.reparse
		REFETCH = args.refetch
		return args.route

	def serve(text, ctype = "text/xml", encoding = "utf-8"):
		print(text)

else:
	import urllib.parse

	def route_from_arg(request):
		# return request.headers["spin-path-info"]
		# 'http://localhost:3000/weforum?reset='
		uri = urllib.parse.urlparse(request.headers["spin-full-url"])
		print(uri.path, urllib.parse.parse_qsl(uri.query))
		return uri.path + "?" + uri.query

	def serve(text, ctype = "text/xml", encoding = "utf-8"):
		return Response(200, {"content-type": ctype}, bytes(text, encoding))


def is_dev():
	with open('spin.toml') as file:
		m = re.search('^name\s*=\s*".+?-dev"', file.read(), re.M)
		return not not m


def reset_store(parser):
	store = Store(parser.URL)
	# print(store.age)
	# print(len(store.atom))
	ok = False
	if store.atom:
		print(f'Resetting {store.prefix}.atom')
		store.atom = ""
		ok = True
	if store.text:
		print(f'Resetting {store.prefix}.text')
		store.text = ""
		ok = True
	return ok


def split_route(text):
	split = text.split('?')
	if len(split) == 1:
		return text, ""
	return split[0], split[1]


def parse_query(text):
	# NOTE: The python lib is insufficient here.
	#		It requires a value for a key and it
	#		returns a list, not a dict.
	# 	import urllib.parse
	# 	return route, urllib.parse.parse_qsl(text)
	args = {}
	for kv in text.split('&'):
		m = re.match('([^=]+)(?:=(.+))?', kv)
		if m:
			args[m.group(1)] = m.group(2)
	return args


def parser_from_route(route):
	for parser in parsers:
		if re.match(r'^/%s(/.*)?$' % parser.__name__, route):
			return parser


def atom_from_parser(parser):
	store = Store(parser.URL)
	print(store.age)
	atom = store.atom

	if OFFLINE:
		if REPARSE:
			atom = parser.parse(store.text)
	elif REPARSE:
		atom = parser.parse(store.text)
		store.atom = atom
	elif REFETCH or not store.text or not store.atom or store.expired:
		text = fetch(parser.URL, parser.HEADERS)
		store.text = text
		atom = parser.parse(text)
		store.atom = atom

	return atom


def handle_request(request):
	route = route_from_arg(request)
	route, query = split_route(route)
	parser = parser_from_route(route)

	# print(route, query)

	if is_dev():
		args = parse_query(query)
		print(route, args)
		if 'reset' in args:
			ok = reset_store(parser)
			return serve('Done.' if ok else 'Nothing to do.', "text/plain")

	if not parser:
		routes = ", ".join("/" + parser.__name__ for parser in parsers)
		return serve(f'No such feed: "{route}". Try one of: {routes}.', "text/plain")

	atom = atom_from_parser(parser)
	return serve(atom)


if __name__ == "__main__":
	sys.exit(handle_request(None))
