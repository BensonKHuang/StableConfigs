# Monomer Class


class Monomer:
    # CONSTRUCTOR
    def __init__(self, tbn_problem, binding_sites):  # binding_sites = [BindingSite, BindingSite, ...]
        # increment unique_id
        tbn_problem.monomer_count = tbn_problem.monomer_count + 1

        # parent all sites
        for BindingSite in binding_sites:
            BindingSite.ParentMonomer = self

        # constructor
        self.name = None
        self.id = tbn_problem.monomer_count
        self.BindingSites = binding_sites

        # add monomer to lis
        tbn_problem.all_monomers.append(self)

    def get_max(self, other):
        return self if self.id > other.id else other


    def __str__(self):
        monomer_name = ("\t>" + self.name) if self.name is not None else ""
        return (str(list(map(lambda x: str(x), self.BindingSites))) + monomer_name)

    def to_json_format(self):
        cur_monomer = []
           # A BindingSite's name (if it has one) is appended to the end of the site string (a*:name).
        for binding_site in self.BindingSites:
            cur_monomer.append(str(binding_site))
        # A monomer's name (if it has one) is the last element of the BindingSite list, starting with a '>'.
        if self.name is not None:
            cur_monomer.append(">" + self.name)

        return cur_monomer