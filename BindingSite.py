# BindingSite Class


class BindingSite:
    # CONSTRUCTOR

    def __init__(self, tbn_problem, str_site):  # str_site = "a*", "b", etc.
        # increment unique_id
        tbn_problem.site_count = tbn_problem.site_count + 1

        # check if complement
        find_comp = str_site.find('*')
        has_comp = True
        if find_comp == -1:
            find_comp = len(str_site)
            has_comp = False

        # grab the name of the binding site
        site_name = str_site[0:find_comp]

        # constructor
        self.id = tbn_problem.site_count
        self.name = site_name
        self.IsComplement = has_comp
        self.ParentMonomer = None
