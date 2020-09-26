__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

import collections


class MemberContainer(collections.UserDict):
    
    def __init__(self):
        
        super(MemberContainer, self).__init__()
        print(f"#111222111 new initialized dict: {repr(self)}")

    def getUser(self, member_url):
        return self.get(member_url, False)

    def setUser(self, member_url, member_name):
        self.update({member_url: {"name": member_name, "url": member_url}})

    def giveStammbezirk(self, member_url, stammbezirk):
        self[member_url].update({"stammbezirk": stammbezirk})

    def giveSchlafmuetze(self, member_url):
        self[member_url].update({"schlafmuetze":True})

    def removeSchlafmuetze(self, member_url):
        del self[member_url]["schlafmuetze"]

    def allMembersSortedByName(self):
        names_to_urls = [(self[member_url]["url"], self[member_url]["name"]) for member_url in self.keys()]
        sorted_names_to_urls = sorted(names_to_urls, key=lambda x: x[1])
        return [(name, url) for url, name in sorted_names_to_urls]

    def updateUser(self, user_url, update_dict):
        self[user_url].update(update_dict)

