# Bind Monomer class
from src.common.Monomer import Monomer


class Rep(object):

	def __init__(self, monomer: Monomer):
		self.monomer = monomer

	def __eq__(self, other):
		return self.monomer.id == other.monomer.id

	def __hash__(self):
		return hash(self.monomer.id)
