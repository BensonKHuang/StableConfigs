# BindingSite Class


class BindingSite:
    unique_id = 0
    site_names_count = dict()
    site_complement_count = dict()

    # CONSTRUCTOR

    def __init__(self, str_site):  # str_site = "a*", "b", etc.
        # increment unique_id
        BindingSite.unique_id = BindingSite.unique_id + 1

        # check if complement
        find_comp = str_site.find('*')
        has_comp = True
        if find_comp == -1:
            find_comp = len(str_site)
            has_comp = False

        # grab the name of the binding site and put it in the dictionaries
        site_name = str_site[0:find_comp]
        if site_name not in BindingSite.site_names_count:
            BindingSite.site_names_count[site_name] = 0
            BindingSite.site_complement_count[site_name] = 0

        BindingSite.site_names_count[site_name] = BindingSite.site_names_count[site_name] + 1
        if has_comp:
            BindingSite.site_complement_count[site_name] = BindingSite.site_complement_count[site_name] + 1

        # constructor
        self.id = BindingSite.unique_id
        self.name = site_name
        self.IsComplement = has_comp
        self.ParentMonomer = None

    # STATIC

    @staticmethod
    def get_limiting_site():
        current_site = None
        current_min = None

        for site_name in BindingSite.site_names_count:
            num_site = BindingSite.site_names_count[site_name] - BindingSite.site_complement_count[site_name]
            num_comp = BindingSite.site_complement_count[site_name]

            if (current_site is None) or (current_min > num_site or current_site > num_comp):
                current_site = site_name if num_site <= num_comp else (site_name + "*")
                current_min = num_site if num_site <= num_comp else num_comp

        return current_site
