import sys, os, re, argparse

import aldaily
import ibtimes
import weforum
parsers = [ aldaily, ibtimes, weforum ]

from lib.fetch import fetch
from lib.Store import Store


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
	def route_from_arg(request):
		return request.headers["spin-path-info"]

	def serve(text, ctype = "text/xml", encoding = "utf-8"):
		return Response(200, {"content-type": ctype}, bytes(text, encoding))


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
	parser = parser_from_route(route)

	if not parser:
		routes = ", ".join("/" + parser.__name__ for parser in parsers)
		return serve(f'No such feed: "{route}". Try one of: {routes}.', "text/plain")

	atom = atom_from_parser(parser)
	return serve(atom)


if __name__ == "__main__":
	sys.exit(handle_request(None))
