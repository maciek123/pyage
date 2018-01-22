import logging
logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NamingService(object):
	__metaclass__ = Singleton
	def __init__(self,starting_number):
		self.counter = starting_number

	def get_next_agent(self):
		old = self.counter
		self.counter += 1
		return str(old)