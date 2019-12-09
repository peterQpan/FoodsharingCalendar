import datetime
import sys
import time
from platform import system
from tkinter import messagebox
from warnings import warn
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from events import Event

class PlatformDriver(webdriver.Firefox):
    def __init__(self, dev=False):
        if dev:
            super().__init__(executable_path="./geckolinux/geckodriver")
        else:
            option = Options()
            option.add_argument("--headless")

            if "Linux" in system():
                super().__init__(
                    executable_path="./geckolinux/geckodriver", options=option)
            elif "Win" in system():
                super().__init__(
                    executable_path=".\\geckowin\\geckodriver.exe",options=option)
            elif "OS" in system():
                messagebox.showinfo("Apple?!?", "Pech!!! :P")
                time.sleep(sys.maxsize)
                sys.exit(666)
            else:
                if messagebox.showinfo("Unbekanntes Betriebssystem", "Support:\nsebmueller.sb@gmail.com "):
                    sys.exit(0)

class JsFoodsharingSiteScraperFireFox:
    #No error handeling, its better to crash, than do something wrong when creating
    # Events, furthermore Events with google.location with route

    def __init__(self, webdriver, queue, main_window):
        self.main_window = main_window
        self.queue = queue
        self.dates = []
        self.companys = []
        self.addresses = []
        self.start_url = 'https://beta.foodsharing.de/'
        self.webdriver = webdriver
        self._events = None
        self.personal_informations_site = None
        self.first =None

        queue.put("https://beta.foodsharing.de/ Verbindung hergestellt")

    def logingIn(self, login_name, password, first):
        self.webdriver.get(self.start_url)
        self.webdriver.find_element_by_id("login-email").send_keys(login_name)
        self.webdriver.find_element_by_id("login-password").send_keys(password)
        self.webdriver.find_element_by_class_name("btn.btn-secondary.btn-sm").click()

        self.queue.put("Erfolgreich eingeloggt")
        while self.start_url == self.webdriver.current_url:
            time.sleep(0.1)
        self.start_site = self.webdriver.current_url

        if first:
            self.webdriver.get("https://beta.foodsharing.de/profile/315541")
            while self.start_site == self.webdriver.current_url:
                time.sleep(0.1)
            try:
                button = self.webdriver.find_element_by_partial_link_text("Ich kenne")
                button.click()
                self.queue.put("Als Nutzer des Programms registriert")
                self.main_window.counterUpdate()
            except:
                pass
        self.personal_informations_site = self.goToPersonalInformations()

    def goToPersonalInformations(self):
        self.webdriver.get(self.start_site)
        while self.start_site != self.webdriver.current_url:
            time.sleep(0.1)
        time.sleep(0.3)
        self.webdriver.find_element_by_partial_link_text("Hallo").click()
        while self.start_site == self.webdriver.current_url:
            time.sleep(0.1)
        return self.webdriver.current_url

    def gatherTimesAndCompanys(self):
        self.webdriver.get(self.personal_informations_site)
        content_box = self.webdriver.find_element_by_id("double")
        date_snipets = content_box.find_elements_by_tag_name("a")
        assert len(date_snipets) % 3 == 0
        dates = [x for i, x in enumerate(date_snipets) if i % 3 == 0]
        companys = [x for i, x in enumerate(date_snipets) if i % 3 == 1]
        assert len(dates) == len(companys)
        return dates, companys

    def gatherAppointmentInfos(self):
        java_bullshit_counter = 0
        self.webdriver.set_window_size(2000, 6000)
        while True:
            dates, companys = self.gatherTimesAndCompanys()
            self.dates.append(dates[java_bullshit_counter].text)
            self.companys.append(companys[java_bullshit_counter].text)
            dates[java_bullshit_counter].click()
            while self.personal_informations_site == self.webdriver.current_url:
                time.sleep(0.1)
            time.sleep(0.2)
            actual_site = self.webdriver.current_url
            adress_nodes = self.webdriver.find_elements_by_class_name("input-wrapper")
            for adress_node in adress_nodes:
                if "Adresse" in adress_node.text:
                    self.addresses.append(adress_node.text)
                    break
            self.queue.put(f"\nTermin geholt:\n{self.dates[java_bullshit_counter]} bei {self.companys[java_bullshit_counter]}\n"
                           f"Adresse: {self.addresses[java_bullshit_counter]}")
            self.main_window.counterUpdate()

            self.webdriver.get(self.personal_informations_site)
            while actual_site == self.webdriver.current_url:
                time.sleep(0.1)
            if java_bullshit_counter == len(dates) -1:
                break
            else:
                java_bullshit_counter += 1
        self.queue.put(f"Alle Termine geholt")

    def standarizeDate(self, date_string): #datetime.datetime
        jetzt = time.localtime()
        dm = {"year":jetzt[0], "Dez":12, "Nov":11, "Okt":10, "Sep":9, "Aug":8, "Jul":7, "Jun":6, "Mai":5, "Apr":4, "Mär":3, "Feb":2,
              "Jan":1, "Tag":jetzt[2], "month":jetzt[1]}
        jetzt_list = list(jetzt)[:-2]
        heute = datetime.datetime(*jetzt_list)
        date = date_string.replace(".", "")
        date = date.replace(",", "")
        date = date.split()
        if len(date) == 4:
            zeit = [int(x) for x in date[2].split(":")]
            iso_date = datetime.datetime(dm["year"], dm["month"], dm["Tag"], zeit[0], zeit[1])
            if date[1] == "Heute":
                return iso_date
            else:
                return iso_date + datetime.timedelta(days=1)
        else:
            date[2] = int(date[2])
            zeit = [int(x) for x in date[4].split(":")]
            iso_date = datetime.datetime(dm["year"], dm[date[3]], date[2], zeit[0], zeit[1])
            ### ist der hauptgrund warum ich kein vorhandenes modul benutze, teilweise keine jahresangaben,
            # also muss wieder sicher gegangen werden
            if iso_date < heute - datetime.timedelta(days=2):
                return datetime.datetime(dm["year"] + 1, dm[date[3]], date[2], zeit[0], zeit[1])
            else:
                return iso_date

    def createEvents(self):
        self.personal_informations_site = self.goToPersonalInformations()
        self.gatherAppointmentInfos()
        events = []
        delta = datetime.timedelta(minutes=45)
        for company, date, addresse in zip(self.companys, self.dates, self.addresses):
            date = self.standarizeDate(date)
            addresse = addresse.replace("Adresse\n", "")
            addresse = addresse.replace("\n", " ")
            events.append(Event(start=date, end=date + delta, summary=company, description="", location=addresse))
        self._events = events
        self.queue.put(f"alle Foodsharing-Termine in vergleichbare Events verwandelt")
        return events

    def existingEvents(self):
        counter = 10
        while counter:
            if self._events:
                return self._events
            else:
                time.sleep(0.2)
        warn("es muss zuerst createEvents ausgeführt werden", category=RuntimeWarning)

