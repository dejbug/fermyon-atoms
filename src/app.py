import io, os

from spin_http import Response, Request, http_send

#~ import ibt

def fetch():
	response = http_send(Request("GET", ibt.Page.URL, ibt.Page.HEADERS, None))
	return response.body.decode("utf8") if response.status == 200 else None

def parse(text):
	buffer = io.StringIO()
	ibt.rss(text, buffer)
	return buffer.getvalue()


def handle_request(request):
	print(dir())

	#~ print(dir(request), request.method, request.headers)
	route = request.headers["spin-component-route"].strip("/")
	#~ print(route)

	#~ rate = int(os.environ["RATE"])
	#~ print(rate)

	store = Store(route)
	#~ print(store.age)

	if store.expired:
		text = fetch()
		rss = parse(text)
		store.rss = rss
	else:
		rss = store.rss

	return Response(200, {"content-type": "text/xml"}, bytes(rss, "utf-8"))
	#~ return Response(200, {"content-type": "text/plain"}, bytes("No such feed.", "utf-8"))
