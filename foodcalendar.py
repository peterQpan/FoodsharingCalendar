import datetime
import re
import sys
import time

from pip._vendor.colorama import Fore

import content
import fs_site_scraper
import fs_site_scraper as fss
import google_tools
import modification


import PySimpleGUI as sg

import sc
from fs_site_scraper import JsFoodsharingSiteScraper

sg.theme("DarkTanBlue")


def googleCalendarMain():

    now_time = datetime.datetime(*time.localtime()[:6])

    fs_site_scraper = fss.JsFoodsharingSiteScraper(
            login_name=modification.email(), password=modification.psd(),
            programm_used_first_time=modification.programmUsedFirst(), debug=modification.debug())
    all_fs_events = fs_site_scraper.allFsEvents()
    for event in all_fs_events:
        print(event)

    google_calender_connection = google_tools.MyGoogleCalendarConnection()
    all_google_events = google_calender_connection.fetchEvents(min_time=now_time)

    new_events, maybe_changed_events, conflicting_events = google_tools.Event.compareFsWithGoogleEvents(all_fs_events, all_google_events)

    print(f"NEW EVENTS:\n{new_events}\n\n\n")
    print(f"{Fore.YELLOW}maybe_changed\n{maybe_changed_events}\n\n\n")
    print(f"{Fore.RED}conflictiong_events:\n{conflicting_events}\n\n\n”{Fore.RESET}")

    for event in new_events:
        google_calender_connection.createGoogleEvent(event)








class GoogleCalendarMainGui():
    site_scraper: JsFoodsharingSiteScraper

    def __init__(self):
        self.actual_time = datetime.datetime(*time.localtime()[:6])

        self.completeRun()

    def oneEventClassString(self, events, if_not_string, else_string):
        string_here = ""
        if not events:
            string_here += if_not_string
        else:
            string_here += else_string
            for event in events:
                eins, zwei = event
                if not zwei:
                    string_here += f"{event[0]}\n"
                else:
                    string_here += f"Termin1: {eins}\nmit\nTermin2: {zwei}\n\n"
                # except Exception as e:
                #     print(f"{Fore.RED}ERROR #90i32jkjn32fd -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")

        string_here += "\n" * 3
        return string_here

    def guiFinalNotification(self, *all_events):
        final_sting = ""
        if_not_strings = ("KEINE NEUEN TERMINE", "KEINE VERÄNDERTEN TERMINE", "KEINE KONFLIKTE")
        else_strings = ("NEUE TERMINE:\n", "MÖGLICHERWEISE VERÄNDERTE TERMINE\n", "KONFLIKTE\n")
        for events, if_not_string, else_string in zip(all_events, if_not_strings, else_strings):
            final_sting += self.oneEventClassString(events, if_not_string, else_string)
        return final_sting

    def emailIsNotValidPopup(self):
        invalid_window = sg.Window('Invalid Email',
                                  [[sg.T(text='Invalid Email', size=(25, 1), justification="centered")],
                                   [sg.B('OK'), sg.B(content.cancel())]])
        event = invalid_window.read()
        print(f"event: {event},")
        if content.cancel() in event:
            sys.exit(0)
        if "OK" in event:
            invalid_window.close()
            return True
        invalid_window.close()

    def emailIsValid(self, email):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email)

    def loginWindow(self):
        login_window = sg.Window('Login Window',
                                 [[sg.T(text='Email:', size=(8, 1)), sg.In(key='Email'), ],
                                  [sg.T(text="Passwort:", size=(8, 1)), sg.In(key="psd", password_char="*")],
                                  [sg.Checkbox(text="  Zugangsdaten speichern", key="speichern")],
                                  [sg.B('OK'), sg.B('Cancel')]])
        while True:
            event, values = login_window.read()
            print(f"event: {event}, values: {values}")
            if not self.emailIsValid(values["Email"]):
                 self.emailIsNotValidPopup()
            elif not values["psd"]:
                sg.Print(f"kein Passwort....")
            else:
                break
        login_window.close()
        return values

    def getSavedLoginData(self):
        try:
            email, psd = sc.loadLoginData()
        except TypeError as e:
            print(f"{Fore.RED}ERROR #9032oihho234 --> zugangsdaten konnten nicht geladen werden {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
            email, psd = None, None
        return email, psd

    def completeLogin(self):
        while True:
            email, psd = self.getSavedLoginData()
            if not email:
                values:dict = self.loginWindow()
                email = values["Email"]
                psd = values["psd"]
                if values["speichern"]:
                    sc.saveLoginData(values["Email"], values["psd"])

            # try:
            self.site_scraper = fs_site_scraper.JsFoodsharingSiteScraper(
                    login_name=email, password=psd, programm_used_first_time=modification.programmUsedFirst(),
                    debug=modification.debug())  # todo debug weg

            #     return
            # except Exception as e:
            #     print(f"{Fore.RED}ERROR #23424wedsadsf --> {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
            #     sg.Print(f"FEHLER!!!! Überprüfe zugangsdaten oder Internetverbindung")
            #     break
    @classmethod
    def firstWindow(cls):
        layout = [[sg.Text(content.fistWindowText(), size=modification.firsWindowSize(), justification="center", font=modification.firstWindowFontSize())],
                  [sg.T("  " * 27), sg.Button("Weiter"), sg.Button(content.cancel())]]
        window = sg.Window("FoddCalendar 2.0 / FoodCalendarAutomat 1.0", layout=layout)
        while True:
            event, values = window.read()
            print(f"evant, values: {event}, {values}")
            if event in (None, "Nichts wie weg hier"):
                sys.exit(0)
            else:
                window.close()
                break

    def completeRun(self):
        print(f"complete run: 1")
        now_time = datetime.datetime(*time.localtime()[:6])
        print(f"complete run: 2")
        self.firstWindow()
        print(f"complete run: 3")
        self.completeLogin()
        print(f"complete run: 4")
        all_fs_events = self.site_scraper.allFsEvents()
        print(f"complete run: 5")
        self.google_connection = google_tools.MyGoogleCalendarConnection()
        print(f"complete run: 6")
        all_google_events = self.google_connection.fetchEvents(min_time=now_time)
        print(f"complete run: 7")
        new_events, maybe_changed_events, conflicting_events = google_tools.Event.compareFsWithGoogleEvents(all_fs_events,
                                                                                                            all_google_events)
        print(f"complete run: 8")
        scoll_able = sg.Column(layout=[[sg.Text(text=self.guiFinalNotification(new_events, maybe_changed_events, conflicting_events))]])
        window = sg.Window(layout=[[scoll_able], [sg.Button("Ok"), sg.Button(content.cancel())]],
                           title="Zusammenfassung")
        response = window.read()
        print(response)
        print(f"complete run: 10")

        if response[0] == "Ok":
            print(f"complete run: 11")
            print(print(f"darstellung von n,mc,ce: {(new_events, maybe_changed_events, conflicting_events)}"))
            duplikate_free_events = google_tools.Event.stripDuplicates(maybe_changed_events, conflicting_events, all_google_events)
            all_events = [*new_events, *duplikate_free_events]
            self.google_connection.createEvents(all_events)




if __name__ == '__main__':
    calendar_gui = GoogleCalendarMainGui()


