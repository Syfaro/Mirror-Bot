class SiteHandler:
	def __init__(self):
		self.handlers = {}
		self.config = {}

	def set_config(self, domain, config):
		self.config[domain] = config

	def add_handler(self, domain, handler):
		self.handlers[domain] = handler

	def run_handler(self, thing):
		if thing.domain in self.handlers:
			config = None
			if thing.domain in self.config:
				config = self.config[thing.domain]

			return self.handlers[thing.domain](thing, config)
		else:
			return None