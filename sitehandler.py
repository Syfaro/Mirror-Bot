class SiteHandler:
	def __init__(self):
		"""
		handles loading of different files for different sites with configuration
		"""
		self.handlers = {}
		self.config = {}

	def load_config(self, config):
		"""
		updates the entire configuration dict
		"""
		self.config = config

	def set_config(self, domain, config):
		"""
		sets the configuration dict for a specific domain
		"""
		self.config[domain] = config

	def add_handler(self, domain, handler):
		"""
		registers a handler for a domain
		"""
		self.handlers[domain] = handler

	def run_handler(self, thing):
		"""
		runs the handler for a domain and returns its result
		"""
		if thing.domain in self.handlers:
			config = None
			if thing.domain in self.config:
				config = self.config[thing.domain]

			return self.handlers[thing.domain](thing, config)
		else:
			return None