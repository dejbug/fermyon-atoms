import datetime, os

from spin_key_value import kv_open_default

DEFAULT_RATE = 3600


class Store:
	def __init__(self, prefix, encoding = "utf-8"):
		self.rss_key = prefix + ".rss"
		self.time_key = prefix + ".time"
		self.encoding = encoding
		self.store = kv_open_default()

	@property
	def rate(self, default = DEFAULT_RATE):
		return float(os.environ["RATE"] if "RATE" in os.environ else default)

	@property
	def now(self):
		return datetime.datetime.now(datetime.timezone.utc).timestamp()

	@property
	def text(self):
		return ""

	@text.setter
	def text(self, text):
		pass

	@property
	def rss(self):
		rss = self.store.get(self.rss_key)
		return str(rss, self.encoding) if rss else ""

	@rss.setter
	def rss(self, rss):
		self.store.set(self.rss_key, bytes(rss, self.encoding))
		self.update()

	@property
	def time(self):
		time = self.store.get(self.time_key)
		return float(time) if time else 0.0

	@property
	def age(self):
		return self.now - self.time

	@property
	def expired(self):
		return self.age > self.rate

	def update(self):
		self.store.set(self.time_key, bytes(str(self.now), self.encoding))
