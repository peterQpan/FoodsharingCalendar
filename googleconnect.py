import datetime
import json
import os.path
import pickle
import sys
import time
import tkinter.messagebox
import warnings
from time import strptime
from warnings import warn

from PySimpleGUI import Print
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pip._vendor.colorama import Fore


import randomone
from google_tools import Event
from randomone import SomethingDing


class GoogleEventCalendar:
    scope = 'https://www.googleapis.com/auth/calendar.events'
    def __init__(self, dev_creds=None, dev_token=None, queue_here=randomone.DevQueue()):
        self.queue = queue_here
        self.entry_token = dev_token if dev_token else 'token.pickle'
        self.creds = dev_creds if dev_creds else 'credentials.json'
        self._events = None
        self.connection = None
        self.working = True

    def connect(self):
        self.connection = self._connect()
        return self.connection

    def _connect(self, break_next=False):
        try:
            creds = None
            if os.path.exists(self.entry_token):
                with open(self.entry_token, 'rb') as token:
                    creds = pickle.load(token)
                    self.queue.put(f"Google Credentials geladen")
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    self.queue.put(f"Google Zuganng muss gewährt werden")
                    creds.refresh(Request())
                else:
                    some = SomethingDing("filas2.tsm", something="lauterszeug")
                    flow = InstalledAppFlow.from_client_config(
                            json.loads(some.load()[0]), self.scope)

                    self.queue.put(f"Google Verbindung hergestellt")
                    creds = flow.run_local_server(port=0)
                with open(self.entry_token, 'wb') as token:
                    pickle.dump(creds, token)
                    self.queue.put(f"Google Credentials gespeichert")
            self.working = False

        except Exception as e:
            print(f"{Fore.RED}ERROR #aiuii8uljkne23 -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
            Print("Probleme sich mit Google zu verbinden, oder Berechtigung zu erhalten")


            if not break_next:
                #just a second try to connect
                try:
                    os.remove(self.entry_token)
                except FileNotFoundError as e:
                    print(f"{Fore.RED}ERROR #ölasuw90oih234 -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
                return self._connect(break_next=True)
            else:
                if Print("Sorry!!!! Etwas ist schief gegangen, versuche es nochmal!!!"):
                    sys.exit(666)
        return build('calendar', 'v3', credentials=creds)


    def _gaterGoogleEvents(self):

        jetzt = datetime.datetime(*list(time.localtime())[:-2]) - datetime.timedelta(hours=1) #WTF this is verry ugly
        #Todo sollte ich das hier wirklich ernsthaft vorantreiben wollen ist das ja wohl eins der ersten dinge die ich
        # ändern sollte.... zeit-internationalisierung.... FU :'D xD
        than = jetzt + datetime.timedelta(days=60)
        jetzt = str(jetzt).replace(" ", "T") + "Z"
        than = str(than).replace(" ", "T") + "Z"


        events_result = self.connection.events().list(
                calendarId='primary', timeMin=jetzt, timeMax=than,
                singleEvents=True, orderBy='startTime')\
                    .execute()
        self.queue.put(f"Termine der nächsten 2 Monate von Google geholt")

        return events_result["items"]

    def fetchExistingEvents(self):
        self.connection = self.connect()
        events = []
        for g_event in self._gaterGoogleEvents():
            #todo der slice auf 19 wird noch probleme bereiten!!!
            # trotzdem bring es erstmal fertig dass es läuft, danach kannst du dich um die eine stunde immer
            # noch kümmern... wenns nicht läuft weisst auch das endergebnis nicht und wo zu schrauben
            try:
                start = strptime(g_event["start"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
                start = datetime.datetime(*list(start)[:6])
                end = strptime(g_event["end"]["dateTime"][:19], "%Y-%m-%dT%H:%M:%S")
                end = datetime.datetime(*list(end)[:6])
            except Exception as e:
                print(f"{Fore.RED}ERROR #902ij3ölknads -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")

                try:
                    start = strptime(g_event["start"]["date"][:10], "%Y-%m-%d")
                    start = datetime.datetime(*list(start)[:3])
                    end = start + datetime.timedelta(days=1)
                except Exception as e:
                    print(f"{Fore.RED}ERROR #90092i4joilj45 --> {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
                    Print(f"Unübliches ereigniss bitte sende die folgenden Zeilen an sebmueller.sb@gmail.com:\n\n{g_event}\n\nDanke")
                    continue

            print(f"{start} bis {end}")
            otw = []
            for tag in ("summary", "description", "location"):
                try:
                    otw.append(g_event[tag])
                except KeyError as e:
                    print(f"{Fore.RED}ERROR #kß923oijksdfas -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
                    otw.append("")
            events.append(Event(start=start, end=end, summary=otw[0], description=otw[1], location=otw[2]))

        [print(e) for e in events]
        self.queue.put(f"Google Termine stehen jetzt zum Vergleich bereit")

        self._events = events
        return

    def existingEvents(self):
        counter = 30
        while counter:
            if not self._events:
                time.sleep(.2)
                counter -= 1
            else:
                return self._events
        warn(message=f"fetchExistingEvents muss zuerst aufgerufen werden",
             category=RuntimeWarning)

    def eventDummy(self):

        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2020-05-28T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2015-05-28T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

    def createEvent(self, event):

        start = f"{event.start}".replace(" ", "T")
        end = f"{event.end}".replace(" ", "T")

        body = {
            'summary': event.summary,
            'location': event.location,
            'description': event.description,
            'start': {
                'dateTime': start,
                'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Europe/Berlin',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 4 * 60},
                    {'method': 'popup', 'minutes': 45},
                ],
            },
        }

        event = self.connection.events().insert(calendarId='primary', body=body).execute()
        'Event created: %s' % (event.get('htmlLink'))

    def createEventDummy(self):
        event = self.connection.events().insert(calendarId='primary', body=self.eventDummy()).execute()
        'Event created: %s' % (event.get('htmlLink'))


if __name__ == "__main__":
    googleService = GoogleEventCalendar()
    print(googleService.fetchExistingEvents())

    googleService.createEventDummy()
    #
    # event = Event(datetime.datetime(2019, 12, 12, 12, 12, 12), datetime.datetime(2019, 12, 12, 12, 45, 12),
    #               "endgültiger Test", "wenn das hier klappt bin ich  fertig", location="Nauwieserstr. 17, 66611 Saarbrücken")
    # googleService.createEvent(event)

