# Bind Monomer class
from stableconfigs.common.Monomer import Monomer


class Bind(object):

	def __init__(self, monomer1: Monomer, monomer2: Monomer):
		self.monomer1 = monomer1
		self.monomer2 = monomer2

	def __eq__(self, other):
		return {self.monomer1.id, self.monomer2.id} == {other.monomer1.id, other.monomer2.id}

	def __hash__(self):
		return hash(frozenset([self.monomer1.id, self.monomer2.id]))

	def get_symmetric_difference(self, other):
		return {self.monomer1, self.monomer2}.symmetric_difference({other.monomer1, other.monomer2})
