import argparse, re, sys

import aldaily
import ibtimes
import weforum

from fetch import fetch
from Store import Store


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


def module_from_route(route):
	if re.match(r'^/aldaily(/.*)?$', route):
		return aldaily
	if re.match(r'^/ibtimes(/.*)?$', route):
		return ibtimes
	if re.match(r'^/weforum(/.*)?$', route):
		return weforum


def atom_from_module(module):
	store = Store(module.URL)
	atom = store.atom

	if OFFLINE:
		if REPARSE:
			atom = module.parse(store.text)
	elif REPARSE:
		atom = module.parse(store.text)
		store.atom = atom
	elif REFETCH or not store.text or not store.atom or store.expired:
		text = fetch(module.URL, module.HEADERS)
		store.text = text
		atom = module.parse(text)
		store.atom = atom

	return atom


def handle_request(request):
	route = route_from_arg(request)
	module = module_from_route(route)

	if not module:
		return serve(f'No such feed: "{route}".', "text/plain")

	atom = atom_from_module(module)
	return serve(atom)


if __name__ == "__main__":
	sys.exit(handle_request(None))
