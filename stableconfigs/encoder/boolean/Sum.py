# Bind Monomer class


class Sum(object):

	def __init__(self, rep_index, min_reps):
		self.rep_index = rep_index
		self.min_reps = min_reps

	def __eq__(self, other):
		return self.rep_index == other.rep_index and self.min_reps == other.min_reps

	def __hash__(self):
		return hash((self.rep_index, self.min_reps))

