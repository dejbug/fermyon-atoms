import datetime, os

DEFAULT_RATE = 3600


class FileStore:
	def __init__(self):
		pass

	def get(self, key):
		if os.path.isfile(key):
			with open(key, "rb") as file:
				return file.read()

	def set(self, key, val):
		with open(key, "wb") as file:
			file.write(val)


class Store:
	def __init__(self, prefix):
		self.rss_key = prefix + ".rss"
		self.time_key = prefix + ".time"
		self.store = FileStore()

	@property
	def rate(self, default = DEFAULT_RATE):
		return float(os.environ["RATE"] if "RATE" in os.environ else default)

	@property
	def now(self):
		return datetime.datetime.now(datetime.timezone.utc).timestamp()

	@property
	def rss(self):
		rss = self.store.get(self.rss_key)
		return str(rss, "utf-8") if rss else ""

	@rss.setter
	def rss(self, rss):
		self.store.set(self.time_key, bytes(str(self.now), "utf-8"))
		self.store.set(self.rss_key, bytes(rss, "utf-8"))

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
