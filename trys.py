__author__ = "Sebastian Müller"
__copyright__ = "Just Me"
__email__ = "sebmueller.bt@gmail.com"

from google_tools import MyGoogleCalendarConnection

google_connection =MyGoogleCalendarConnection()

short, all = google_connection.getCalendarIDs("erd0iddb9r94h6naldkl6vibvg@group.calendar.google.com")

print(f"short: {short}")
print(f"all: {all}")