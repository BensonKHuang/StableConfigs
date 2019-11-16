from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.Polymer import Polymer
from stableconfigs.encoder.SATProblem import SATProblem


def decode_boolean_values(tbn: TBNProblem, sat: SATProblem):
    monomer_to_polymer = dict()

    # Filter for all true monomer representatives
    for boolean in sat.result:
        if boolean > 0 and boolean in sat.id_to_rep.keys(): 
            polymer = Polymer()
            monomer = sat.id_to_rep[boolean].monomer
            monomer_to_polymer[monomer] = polymer
            polymer.add_monomer(monomer)

    # Add remaining monomers to an associated polymer
    for boolean in sat.result:

        # Due to the transitive property, all monomers has a bind to a monomer representative
        if boolean > 0 and boolean in sat.id_to_bind.keys():
            monomer1 = sat.id_to_bind[boolean].monomer1
            monomer2 = sat.id_to_bind[boolean].monomer2

            # Ignore if monomer is binding to itself
            if monomer1 == monomer2: 
                continue

            # Add monomer to existing polymer
            if monomer1 in monomer_to_polymer.keys():
                monomer_to_polymer[monomer1].add_monomer(monomer2)

            # Add monomer to existing polymer
            if monomer2 in monomer_to_polymer.keys():
                monomer_to_polymer[monomer2].add_monomer(monomer1)
                
    return monomer_to_polymer.values()
