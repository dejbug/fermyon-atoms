DEFAULT_USER_AGENT = "X"

def has_key(dict, key):
	return key.lower() in map(str.lower, dict.keys())

try:
	from spin_http import http_send, Request

	def fetch(uri, headers = None):
		headers = headers or {}
		if not has_key(headers, "User-Agent"):
			headers["User-Agent"] = DEFAULT_USER_AGENT
		res = http_send(Request("GET", uri, headers, None))
		return res.body.decode("utf8") # if res.status == 200 else None

except:
	from urllib.request import urlopen, Request

	def fetch(uri, headers = None):
		headers = headers or {}
		if not has_key(headers, "User-Agent"):
			headers["User-Agent"] = DEFAULT_USER_AGENT
		req = Request(uri, headers = headers)
		res = urlopen(req)
		return res.read().decode("utf8") # if res.status == 200 else None
