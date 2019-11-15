from src.common.TBNProblem import TBNProblem
from src.common.Polymer import Polymer
from src.encoder.SATProblem import SATProblem


def decode_boolean_values(tbn: TBNProblem, sat: SATProblem):
    monomer_to_polymer = dict()
    for boolean in sat.result:
        if boolean > 0 and boolean in sat.id_to_rep.keys(): 
            polymer = Polymer()
            monomer = sat.id_to_rep[boolean].monomer
            monomer_to_polymer[monomer] = polymer
            polymer.add_monomer(monomer)

    for boolean in sat.result:
        if boolean > 0 and boolean in sat.id_to_bind.keys():
            monomer1 = sat.id_to_bind[boolean].monomer1
            monomer2 = sat.id_to_bind[boolean].monomer2
            if monomer1 == monomer2: 
                continue
            if monomer1 in monomer_to_polymer.keys():
                monomer_to_polymer[monomer1].add_monomer(monomer2)
            if monomer2 in monomer_to_polymer.keys():
                monomer_to_polymer[monomer2].add_monomer(monomer1)
                
    return monomer_to_polymer.values()