from spin_http import http_send, Request

def fetch(url, headers):
	res = http_send(Request("GET", url, headers, None))
	return res.body.decode("utf8") if res.status == 200 else None
