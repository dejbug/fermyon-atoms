from spin_http import http_send, Request

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.5",
	"Accept-Encoding": "identity",
	#~ "Connection": "close",
}

def fetch(url, headers = HEADERS):
	res = http_send(Request("GET", url, headers, None))
	return res.body.decode("utf8") if res.status == 200 else None
	#~ req = Request("GET", url, headers, None)
	#~ print(dir(req), req.headers, req.body)
	#~ res = http_send(req)
	#~ print(res.status, res.headers, res.body)
	#~ return res.body.decode("utf8")
