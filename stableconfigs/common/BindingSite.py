# BindingSite Class


class BindingSite:
    
    COMPLEMENT_DELIMITER = "*"
    KEYWORD = ":"
    # CONSTRUCTOR

    def __init__(self, tbn_problem, str_site):  # str_site = "a*", "b", etc.
        # increment unique_id
        tbn_problem.site_count = tbn_problem.site_count + 1

        # check if complement
        find_comp = str_site.find(BindingSite.COMPLEMENT_DELIMITER)
        has_comp = True
        if find_comp == -1:
            find_comp = len(str_site)
            has_comp = False

        # grab the name of the binding site
        site_type = str_site[0:find_comp]

        # constructor
        self.id = tbn_problem.site_count
        self.type = site_type
        self.name = None
        self.IsComplement = has_comp
        self.ParentMonomer = None

    def __str__(self):
        name = (self.KEYWORD + self.name) if self.name != None else ""
        site_print = (self.type + "*") if self.IsComplement else self.type
        return site_print + name
