import datetime
import datetime
import json
import pickle
import os.path
import time
import warnings

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pip._vendor.colorama import Fore

import modification



class Event:
    """
    Representiert einen Termin den man mit anderen Terminen zeitlich vergleichen kann
    und enthält alle nötigen Atribute die Google benötigt um ihn in den googlecalendar einzupflegen
    """
    def __init__(self, start:datetime.datetime, company_name:str, location:str, duration=None,
                 time_boundery:int=modification.timeBoundery(),
                 description:str="", notifications:()=(60, 240, 1440), notif_color:str="green", end=None):

        assert(duration or end), "duration oder end muss gegeben sein um Event exakt beschreiben zu können"
        assert(duration is None or isinstance(duration, int)), "duration muss entweder mit None oder int --> Minuten sein"

        self.f = Fore.MAGENTA
        self.start = start
        self.end = end
        self.company_name = company_name
        self.location = location
        self.duration = duration if duration else None
        self.time_boundery = time_boundery
        self.description = description
        self.notifications = notifications
        self.notif_color = notif_color
        self.hashing_help = str(time.time())

    @property
    def duration(self):
        if self.__dict__["duration"]:
            return self.__dict__["duration"]
        datetime_result = self.end - self.start
        return datetime_result.seconds / 60

    @duration.setter
    def duration(self, value):
        self.__dict__["duration"] = value

    @property
    def end(self):
        if not self.__dict__["end"]:
            return self.start + datetime.timedelta(minutes=self.duration)
        return self.__dict__["end"]

    @end.setter
    def end(self, value:datetime.datetime):
        self.__dict__["end"] = value

    def haveTimeConflictWith(self, other):
        """vergleicht zwei termine ob sie zeitlich zu schaffen sind oder es eher schwierig wird beide zu erledigen
        :param other: google_tools.Event()
        :return: True wenn es zeitlich problematisch wird +/-45min, ansonsten False
        """
        compare_min = self.start - datetime.timedelta(minutes=self.time_boundery)
        compare_max = self.end + datetime.timedelta(minutes=self.time_boundery)
        if other.start > compare_max or other.end < compare_min:
            return False
        else:
            return True

    def mabyChangedApointment(self, other):
        return self.isSameCompany(other)

    def isSameCompany(self, other):
        return self.company_name == other.company_name

    def isSameTime(self, other):
        return self.start.time() == other.start.time()

    def isSameEvent(self, other):
        return self.isSameTime(other) and self.isSameCompany(other)

    def isSameDate(self, other):
        return self.start.date() == other.start.date()

    @classmethod
    def compareFsWithGoogleEvents(cls, fs_events, google_events):
        """compares FsEvents with GoogleEvents
        :param fs_events:
        :param google_events:
        :return: new_events, maybe_changed_time_test_list, conflicting_test_list
        """
        new_events = fs_events[:]

        conflicting_test_list = []
        maybe_changed_time_test_list = []

        for fs_event in fs_events:
            for google_event in google_events:

             if fs_event.isSameDate(google_event):
                    try:
                        if fs_event.isSameEvent(google_event):
                            new_events.remove(fs_event)
                        elif fs_event.mabyChangedApointment(google_event):
                            maybe_changed_time_test_list.append((fs_event, google_event))
                        elif fs_event.haveTimeConflictWith(google_event):
                            conflicting_test_list.append((fs_event, google_event))
                    except:
                         continue
        new_events = [(x, None) for x in new_events]
        return new_events, maybe_changed_time_test_list, conflicting_test_list

    def oneLineAdress(self):
        return self.location.replace("\n", " ")

    def __str__(self):
        return f"<{self.company_name}, {self.start} bis {self.end} {self.duration}min, {self.oneLineAdress()}>"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.description == other.description and self.start == other.start

    def __hash__(self):
        return hash(f"{self} {self.hashing_help}")

    @classmethod
    def stripDuplicates(cls, maybe_changed_events, conflicting_events, all_google_events):
        all_events = [*maybe_changed_events, *conflicting_events]
        itter_double = all_events[:]
        for event_tuple in all_events:
            event, second = event_tuple
            for g_e in all_google_events:
                a_e:Event
                g_e:Event
                if event.isSameEvent(g_e):
                    try:
                        itter_double.remove(event_tuple)
                    except:
                        continue
        return itter_double


class MyGoogleCalendarConnection:
    def __init__(self, auto_connect=True):
        self.f = Fore.BLUE
        self.scope = ['https://www.googleapis.com/auth/calendar'] #nicht in modi, muss zu credentials passen und soll nicht einfach änderbar sein
        self.service = self.connect() if auto_connect else None

    def connect(self):
        """
        connect to google-calendar-api
        :return:
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return build('calendar', 'v3', credentials=creds)

    def createReminderStats(self, popup_minutes=(modification.popupMinutes()), email_minutes=(modification.emailMinutes())):
        """
        creates list that contains notification-stats
        :param popup_minutes: tuple of ints minutes before actual event notification appears as popup
        :param email_minutes: tuple of ints minutes before actual event notification appears as email
        :return:
        """

        print(f"popup_minutes: {popup_minutes}, email_minutes: {email_minutes}")
        assert(len(popup_minutes) + len(email_minutes) <= 5), "maximal 5 Reminder möglich"
        remninder_list = []
        if popup_minutes:
            for minutes in popup_minutes:
                remninder_list.append({'method': 'popup', 'minutes': minutes})
        if email_minutes:
            for minutes in email_minutes:
                remninder_list.append({'method': 'email', 'minutes': minutes})
        return remninder_list

    def _deleteEvents(self, min_time:datetime.datetime, time_delta_in_days:int=60,
                      calender_id:str=modification.calendar_id(), max_results=30):
        """ACHTUNG dev und debugtool"""
        warnings.warn("ACHTUNG du bist dabei im Kalender zu LÖSCHEN!!!!", UserWarning)
        if not input(f"(Y/N)") in ("Y"):
            return

        google_events = self.fetchGoogleEvents(min_time=min_time, calender_id=calender_id,
                                               timedelta_in_days=time_delta_in_days, max_results=max_results,
                                               single_events=True)
        for google_event in google_events:
            self.service.events().delete(calendarId='primary', eventId=google_event["id"]).execute()

    def createEventDict(self, start_time:datetime.datetime, end_time:datetime.datetime, company, description,
                        location, reminder_list, color_id=modification.color_id()):
        """
        :return: google_Event_dict benötigt um service.events().insert zu benutzen
        """
        # event = {
        #     'summary': 'Google I/O 2015',
        #     'location': '800 Howard St., San Francisco, CA 94103',
        #     'description': 'A chance to hear more about Google\'s developer products.',
        #     'start': {
        #         'dateTime': '2015-05-28T09:00:00-07:00',
        #         'timeZone': 'America/Los_Angeles',
        #     },
        #     'end': {
        #         'dateTime': '2015-05-28T17:00:00-07:00',
        #         'timeZone': 'America/Los_Angeles',
        #     },
        #     'recurrence': [
        #         'RRULE:FREQ=DAILY;COUNT=2'
        #     ],
        #     'attendees': [
        #         {'email': 'lpage@example.com'},
        #         {'email': 'sbrin@example.com'},
        #     ],
        #     'reminders': {
        #         'useDefault': False,
        #         'overrides': [
        #             {'method': 'email', 'minutes': 24 * 60},
        #             {'method': 'popup', 'minutes': 10},
        #         ],
        #     },
        # }
        # return event

        event = {
            'summary': company,
            'location': location,
            'description': description,
            'start': {

                'dateTime': self.datetimeToTimeString(start_time)
            },
            'end': {
                'dateTime': self.datetimeToTimeString(end_time)
            },
            'colorId' : color_id,
            'reminders': {
                'useDefault': False,
                'overrides': reminder_list
            },
        }
        return event

    def createEvents(self, events, calender_id=modification.calendar_id(), color_id=modification.color_id()):
        print(f"{self.f}alle events hier in create Events: {events} {Fore.RESET}")
        
        for ev, second in events:
            print(f"googleevent soll erzeugt werden!!!! event: {ev}")
            self.createGoogleEvent(my_event=ev, calender_id=calender_id, color_id=color_id)



    def createGoogleEvent(self, my_event:Event, calender_id=modification.calendar_id(), color_id=modification.color_id()):
        """
        erzeugt google-event aus google_tools.Event()
        :return:
        """
        reminder_stats = self.createReminderStats()

        event = self.createEventDict(start_time=my_event.start, end_time=my_event.end, company=my_event.company_name,
                                          description=my_event.description, location=my_event.location,
                                          reminder_list=reminder_stats, color_id=color_id)
        print(f"nach google soll eingespeist werden: calendar_id: {calender_id}, body: {event}")
        event = self.service.events().insert(calendarId=calender_id, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))


    def datetimeToTimeString(self, date_time:datetime.datetime, offset=2, offset_sighn="+"):
        time_string = str(date_time).replace(" ", "T")
        return time_string + f"{offset_sighn}{offset:02d}:00"

    def timeStringToDateTime(self, time_sting:str):
        """
        wandelt google time_string '2020-05-06T12:00:00+02:00' in datetime_objekt
        '2020-05-06T12:00:00+02:00' bedeutet: es ist tatsächlich 12:uhr bei uns aber es hat einen offset von 2
        zur standard-zeit
        :param time_sting: google_time_strin
        :return: datetime.datetime
        """
        datetime_str, offset_sighn, offset_time = time_sting[:19], time_sting[19:20], time_sting[20:]
        print(f"datetime: {datetime_str}, offset sighn: {offset_sighn}, offset_time: {offset_time}")
        try:
            datetime_object = time.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError as e:
            print(f"{Fore.RED}ERROR #09oi234knjw -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")


            datetime_object = time.strptime(datetime_str, '%Y-%m-%d')

        datetime_object = datetime.datetime(*datetime_object[:6])

        return datetime_object

    def fetchGoogleEvents(self, min_time:datetime.datetime, timedelta_in_days:int=90,
                          calender_id:str=modification.calendar_id(), order_by="startTime",
                          max_results:int=500, single_events=True):
        """
        holt google events und gibt sie im eigenen Event-Datentyp zurück
        :param min_time: zeitpunkt ab welchem events geholt werden sollen
        :param timedelta_in_days: zeitraum für den Events geholt werden sollen
        :param order_by: "startTime"or"updated"
        :param time_boundery: zeitüberhang für termin der zu kurze abfolge erkennbar ewerden lässt
        :return: list(google_events-->dict)
        """
        max_time = min_time + datetime.timedelta(days=timedelta_in_days)
        print(f"{self.f}CalendarId hier!!!!!!!!! : {calender_id} {Fore.RESET}")
        
        raw_google_events = self.service.events().list(
                calendarId=calender_id, timeMin=self.datetimeToTimeString(min_time),
                timeMax=self.datetimeToTimeString(max_time), maxResults=max_results,
                singleEvents=single_events, orderBy=order_by).execute()

        fetched_google_events = raw_google_events.get("items", [])
        print(f"{self.f}fetched_google_events: {fetched_google_events} {Fore.RESET}")
        return fetched_google_events


    def fetchEvents(self, min_time:datetime.datetime, timedelta_in_days:int=90,
                          calender_id:str=modification.calendar_id(), order_by="startTime",
                          max_results:int=500, time_boundery=modification.timeBoundery()):
        """
        holt google events und gibt sie im eigenen Event-Datentyp zurück
        :param min_time: zeitpunkt ab welchem events geholt werden sollen
        :param timedelta_in_days: zeitraum für den Events geholt werden sollen
        :param order_by: "startTime"or"updated"
        :param time_boundery: zeitüberhang für termin der zu kurze abfolge erkennbar ewerden lässt
        :return: list(google_tools.Event()'s)
        """

        events = []
        google_event: dict
        for google_event in self.fetchGoogleEvents(
                min_time=min_time, timedelta_in_days=timedelta_in_days , calender_id=calender_id, order_by=order_by,
                max_results=max_results, single_events=True):

            start = google_event["start"]
            starttime_string = start.get("dateTime", None) if start.get("dateTime", None) else start.get("date", None)
            end = google_event["end"]
            endtime_string = end.get("dateTime", None) if end.get("dateTime", None) else end.get("date", None)

            event = Event(start=self.timeStringToDateTime(starttime_string),
                          end=self.timeStringToDateTime(endtime_string),
                          company_name=google_event["summary"],
                          location=google_event.get("location", " "), duration=None, time_boundery=time_boundery,
                          description=google_event.get("description", ""))
            events.append(event)

        return events


    def getCalendarIDs(self, calendarID):

        complete_answer = self.service.calendarList().get(calendarId=calendarID).execute()
        summary_exzerpt = complete_answer["summary"]
        return summary_exzerpt, complete_answer








if __name__ == '__main__':

    event_a = Event(start=datetime.datetime(*time.localtime()[:6]), company_name="schlecker",
                  location="Adresse", duration=50,
                  time_boundery=45, description="sollte klappen")
    print(f"start: {event_a.start}, end: {event_a.end}, duration: {event_a.duration}")
    print(event_a)

    event_b = Event(start=datetime.datetime(*time.localtime()[:6]), company_name="schlecker",
                  location="Adresse", duration=None,
                  end=datetime.datetime(*time.localtime()[:6]) + datetime.timedelta(minutes=60),
                  time_boundery=45, description="sollte klappen")
    print(f"start: {event_b.start}, end: {event_b.end}, duration: {event_b.duration}")
    print(event_b)

    test_set = set()
    test_set.add((event_a, event_b))
    print(test_set)
    test_set.add((event_b, event_a))
    print(test_set)
    test_set.add((event_a, event_b))
    print(test_set)


    google_connection = MyGoogleCalendarConnection()
    google_events = google_connection.fetchGoogleEvents(min_time=datetime.datetime(*time.localtime()[:6]))
    print(f"google_events: {google_events}")

    now_time = datetime.datetime(*time.localtime()[:6])
    #
    # for i in range(2, 20):
    #     starttime = now_time + datetime.timedelta(minutes=60*i)
    #     event_here = Event(start=starttime, duration=modification.standardDuration(), company_name=f"farbe: {i%12}",
    #                        location="Flaumweg 23,\n66111 Saarbrücken", description="das ist ein test der Teste")
    #     google_connection.createGoogleEvent(event_here, color_id=i%12)
    #
    # my_events = google_connection.fetchEvents(min_time=now_time)
    # for my_event in my_events:
    #     print(my_event)

    google_connection._deleteEvents(now_time-datetime.timedelta(days=3), max_results=260, time_delta_in_days=365)

