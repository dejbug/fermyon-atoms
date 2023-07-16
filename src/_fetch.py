import urllib, urllib.request

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.5",
	"Accept-Encoding": "identity",
	#~ "Connection": "close",
}

def fetch(url, headers = HEADERS):
	req = urllib.request.Request(url, headers = headers)
	res = urllib.request.urlopen(req)
	return res.read().decode("utf8") if res.status == 200 else None
