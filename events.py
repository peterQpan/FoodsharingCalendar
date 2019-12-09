import collections
import datetime
from datetime import timedelta
from pprint import pprint

class Event:
    """represents an Event in time and space, :') and in the google calendar."""
    def __init__(self, start:datetime.datetime, end:datetime.datetime,
                 summary, description, location):
        """
        summary:   headline
        """
        self.start = start
        self.end = end
        self.summary = summary
        self.description = description
        self.location = location

    @classmethod
    def doubleCheck(cls, fs_appointments:list, google_dates:list):
        """
        takes two list of events and compares them to prevent real-time-problems ;)
        return:   defaultdict(comparing_classification:
                        list(set(event, event, ...), list(tuple(event-pair), tuple(event-pair), ...)))
        """
        result = collections.defaultdict(lambda :[set(), []])
        if fs_appointments and google_dates:
            for food_save_appointment in fs_appointments:
                for google_date in google_dates:
                    answer = food_save_appointment == google_date
                    print(f"answer: {answer}, {repr(answer)}")
                    pprint(answer)
                    result[answer][0].add(food_save_appointment)
                    result[answer][1].append((food_save_appointment, google_date))
            fs_appointments_set = set(fs_appointments)
            checked_data = fs_appointments_set - result["doppel"][0]
            return checked_data, result
        else: return fs_appointments, []

    def checkAproximation(self, other, minutes, message):
        """
        to avoid multiple appointments at the same time or a very near time
        (since we are bound to physic laws :D) this function checks
        for an approximation of two dates for "minutes"
        minutes:   amount of minutes which are supposed to get from one appointment to the next
        message:   message that will be return if two dates closer than amount of minutes

        return:    None if two dates are far enough separated else message
        """

        if (other.start - timedelta(minutes=minutes)) < self.start and self.start < (other.end + timedelta(minutes=minutes))\
            or (other.start - timedelta(minutes=minutes)) < self.end and self.end < (other.end + timedelta(minutes=minutes))\
            or (other.start - timedelta(minutes=minutes)) < self.start and self.end < (other.end + timedelta(minutes=minutes)):
            pass
        else:
            return None
        if self.summary == other.summary:
            return "changed_appointment???"
        else:
            return message

    def __str__(self):
        return f"Von {self.start} bis {self.end} bei {self.summary}\n" \
               f"Adresse: {self.location}\n" \
               f"Sonstiges: {self.description}"

    def __repr__(self):
        return f"{self.start} {self.summary}"

    def __eq__(self, other):
        """yes this is probably an abuse of this magic function, BUT.... :D
        since i really compare one to another i think this might be legit as well"""
        if self.start.date() != other.start.date():
            return "single"
        elif repr(self) == repr(other):
            return "doppel"
        elif self.checkAproximation(other, 31, "alarm"):
            return self.checkAproximation(other, 31, "alarm")
        elif self.checkAproximation(other, 46, "warning"):
            return self.checkAproximation(other, 46, "warning")
        else:
            return "single"

    def __hash__(self):
        """
        needed to put an Event in an set, or (may be, not needed till now) as an key of an dict
        """
        return hash(repr(self.summary) + repr(self.start) + repr(self.end))





