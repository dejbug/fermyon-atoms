import datetime, os

from urllib.parse import urlparse


class FileStore:
	def get(self, key):
		if os.path.isfile(key):
			with open(key, "rb") as file:
				return file.read()

	def set(self, key, val):
		with open(key, "wb") as file:
			file.write(val)


try:
	from spin_key_value import kv_open_default
except:
	BACKEND = FileStore
else:
	BACKEND = kv_open_default


HEADERS = {}
ENCODING = "utf-8"
RATE = 3600


class Store:
	def __init__(self, uri, headers = HEADERS, encoding = ENCODING, backend = BACKEND):
		prefix = self.prefix_from_uri(uri)
		self.atom_key = prefix + ".atom"
		self.time_key = prefix + ".time"
		self.text_key = prefix + ".text"
		self.store = backend()
		self.encoding = encoding

	@classmethod
	def prefix_from_uri(cls, uri):
		host = urlparse(uri).netloc
		return host.split(".")[-2]

	@property
	def rate(self, default = RATE):
		return float(os.environ["RATE"] if "RATE" in os.environ else default)

	@property
	def now(self):
		return datetime.datetime.now(datetime.timezone.utc).timestamp()

	@property
	def text(self):
		s = self.store.get(self.text_key)
		return str(s, self.encoding) if s else ""

	@text.setter
	def text(self, s):
		if isinstance(s, str):
			s = bytes(s, self.encoding)
		if isinstance(s, bytes):
			self.store.set(self.text_key, s)
			self.update()
		return s

	@property
	def atom(self):
		s = self.store.get(self.atom_key)
		return str(s, self.encoding) if s else ""

	@atom.setter
	def atom(self, s):
		self.store.set(self.atom_key, bytes(s, self.encoding))
		self.update()

	@property
	def time(self):
		s = self.store.get(self.time_key)
		return float(s) if s else 0.0

	@property
	def age(self):
		return self.now - self.time

	@property
	def expired(self):
		return self.age > self.rate

	def update(self):
		self.store.set(self.time_key, bytes(str(self.now), self.encoding))
