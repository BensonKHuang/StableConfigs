
from src.common.BindingSite import BindingSite

class Pair(object):

	def __init__(self, site1 : BindingSite, site2 : BindingSite):
		self.site1 = site1
		self.site2 = site2

	def __eq__(self, other):
		if self.site1.id == other.site1.id and self.site2.id == other.site2.id:
			return true
		if self.site1.id == other.site2.id and self.site2.id == other.site1.id:
			return true
		return false

	def __hash__(self):
		#if not working, check if id is a number
		return hash(str(min(self.site1.id, self.site2.id)) + '+' + str(max(self.site1.id, self.site2.id)))