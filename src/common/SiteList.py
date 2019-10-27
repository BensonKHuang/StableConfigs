# SiteList


class SiteList:
    # CONSTRUCTOR

    def __init__(self, site_name):  # str_site = "a*", "b", etc.
        # constructor
        self._name = site_name
        self._normal_sites = []
        self._complementary_sites = []

    def add(self, site):
        if site.IsComplement:
            self._complementary_sites.append(site)
        else:
            self._normal_sites.append(site)

    # Returns tuple, with first list as limiting sites
    def get_limiting_site_and_non_limiting_site(self):
        if self.get_normal_site_count() <= self.get_complement_site_count():
            return self._normal_sites, self._complementary_sites
        else:
            return self._complementary_sites, self._normal_sites

    def get_total_site_count(self):
        return self._get_complement_site_count() + self._get_normal_site_count()

    def get_complement_sites(self):
        return self._complementary_sites

    def get_complement_site_count(self):
        return len(self._complementary_sites)

    def get_normal_sites(self):
        return self._normal_sites

    def get_normal_site_count(self):
        return len(self._normal_sites)

    def get_site_name(self):
        return self._name
