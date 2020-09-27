__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

# from google_tools import MyGoogleCalendarConnection
#
# google_connection =MyGoogleCalendarConnection()
#
# short, all = google_connection.getCalendarIDs("erd0iddb9r94h6naldkl6vibvg@group.calendar.google.com")
#
# print(f"short: {short}")
# print(f"all: {all}")
import queue

from fs_site_scraper import AllMemberScraper
import email_and_psd

member_scraper = AllMemberScraper(email=None)
member_scraper.member_container = member_scraper.loadContainer()
all_members_sorted = member_scraper.member_container.allMembersSortedByName()
print(all_members_sorted)
member_scraper.initiateWebdriver(debug=True)
member_scraper.logingIn(login_name=email_and_psd.email, password=email_and_psd.psd)
[member_scraper.getAllMemberDataFromSiteUrl(url[1]) for url in all_members_sorted]
# member_scraper.getAllMemberDataFromSiteUrl(all_members_sorted[0][1])
