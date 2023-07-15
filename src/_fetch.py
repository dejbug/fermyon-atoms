import urllib, urllib.request

def fetch(url, headers):
	req = urllib.request.Request(url, headers=headers)
	res = urllib.request.urlopen(req)
	return res.read().decode("utf8") if res.status == 200 else None
