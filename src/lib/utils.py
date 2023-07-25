import re, html

def xml_escape(text):
	text = html.unescape(text)
	text = re.sub(r'&', '&amp;', text, re.S)
	text = re.sub(r'<', '&lt;', text, re.S)
	text = re.sub(r'>', '&gt;', text, re.S)
	text = re.sub(r'\'', '&apos;', text, re.S)
	text = re.sub(r'"', '&quot;', text, re.S)
	return text
