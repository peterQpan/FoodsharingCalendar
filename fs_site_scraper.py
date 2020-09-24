import datetime
import os
import platform
import sys
import time

from pip._vendor.colorama import Fore
from selenium import webdriver
import selenium.webdriver.firefox.options

import google_tools
import modification


class UnknownOS(Exception):
    pass

class CrossPlatformJS_Driver(webdriver.Firefox):
    def __init__(self, debug=modification.debug()): #super() wird in den funktionen gerufen
        self.f = Fore.MAGENTA
        print(f"{self.f}{self.__class__.__name__} geladen {Fore.RESET}")

        self.loadSuatableJavaScripDriverOsDependend(debug=debug)

    def loadSuatableJavaScripDriverOsDependend(self, debug):
        """
        loads the needed JavaScriptPyhtonWebsiteDriver, fitting the used OperatingSystem
        :return:
        """
        options = selenium.webdriver.firefox.options.Options()
        if not debug:
            options.add_argument("--headless")

        if "Linux" in platform.system():
            self.loadRightDriverByBrutforce(path_string=f"./geckolinux/", options=options)
        elif "Win" in platform.system():
            self.loadRightDriverByBrutforce(path_string=".\\geckowin\\", options=options)
        elif "OS" in platform.system():
            print("Apple?!? Pech!!! :P")
            time.sleep(sys.maxsize)
            sys.exit(666)
        else:
            raise UnknownOS

    def loadRightDriverByBrutforce(self, path_string, options):

        drivers = sorted(os.listdir(path_string), reverse=True)

        for driver_file_name in drivers:
            driver_file_path = os.path.join(path_string, driver_file_name)
            try:
                print(f"{self.f}geladen werden soll: {driver_file_path} {Fore.RESET}")
                super().__init__(executable_path=driver_file_path, options=options)
                print(f"{self.f}geladen wurde: {driver_file_path} {Fore.RESET}")
                return
            except Exception as e:
                print(f"{Fore.RED}ERROR #09kölkweröklqw --> Treiber laden fehlgeschlagen {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")




class JsFoodsharingSiteScraper:
    #No error handeling, its better to crash, than do something wrong when creating
    # Events, furthermore Events with google.location with route

    def __init__(self, login_name, password, programm_used_first_time, run_automated=True, debug=modification.debug()):

        #todo vllt sollte man den js_sitescraper sogar noch threaden,
        # wenn er arbeitet während das programm schon mal weiter läuft und gleichzeitig
        # schon mal die google daten holt würde es das ganze ncoh einen tick bewschleunigen

        self.f = Fore.CYAN

        self.programm_used_first_time = programm_used_first_time
        self.personal_informations_url =None
        self.actual_url = None
        self._events = None
        self.first =None

        self.dates = []
        self.companys = []
        self.addresses = []
        self.webdriver = CrossPlatformJS_Driver(debug=debug)

        print(f"{self.f}{self.__class__.__name__} geladen {Fore.RESET}")

        if run_automated:
            self.all_events = self.runCompleteJob(login_name, password)

    @property
    def fs_dashbord_url(self):
        return f"{modification.fsBaseUrl()}{modification.fsDashbordPostfix()}"

    @property
    def profile_id(self):
        try:
            return self.personal_informations_url.split("/")[-1]
        except Exception as e:
            print(f"{Fore.RED}ERROR #90uo43öljknwer -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")

            print(f"{self.f}Es steht noch keine Informationen über die Nutzer_Id bereit {Fore.RESET}")

    def allFsEvents(self):
        return self.all_events

    def closeBrowsdr(self):
        pass





    def gatherTimesCompanysAndCompanySiteUrlsFromPersonalProfilSite(self):
        """sammelt abhol_datums, betriebs namen, und betriebs_seite_urls

        :return: abhol_dates, companies, urls
        """
        self.getSiteByUrl(self.personal_informations_url)

        content_box = self.webdriver.find_element_by_class_name(modification.dateAndCompanyListKey())
        date_company_link_snipets = content_box.find_elements_by_tag_name("a")
        assert len(date_company_link_snipets) % 3 == 0

        abhol_dates = [x.text for i, x in enumerate(date_company_link_snipets) if i % 3 == 0]
        companies = [x.text for i, x in enumerate(date_company_link_snipets) if i % 3 == 1]
        urls = [f"{snipet.get_attribute('href')}" for i, snipet in enumerate(date_company_link_snipets) if i % 3 ==1]

        print(f"{self.f}links: {urls}\ndates: {abhol_dates}\ncompanys: {companies}{Fore.RESET}")
        assert len(abhol_dates) == len(companies) == len(urls)

        return abhol_dates, companies, urls




    def getCompanyAdressFromUrl(self, url):
        """
        :param url: betriebs_url
        :return: string nach dem schema: "Adresse\n<Strase Nr.>\n<PLZ Stadt>
        """
        self.getSiteByUrl(url)
        while True:
            try:
                adress_block = self.webdriver.find_element_by_id("inputAdress")
                print(f"in getCompanyAdresse from url, ausgabe: {adress_block.text}")
                return adress_block.text
            except:
                time.sleep(0.01)


    def isoDateFromDateString(self, date_string): #datetime.datetime
        """
        wandelt den datestring der aus der webseite gezogen wird vollautomatisch in eine vergleichbare und
        per timedelta veränderbares "iso_date" eine datetime.datetime() um

        :param date_string: z.B. '✓ Samstag, 2. Mai, 19:05 Uhr' oder '✓ Morgen, 16:45 Uhr'
        :return: datetime.datetime(2020, 5, 1, 16, 45)
        """

        date = date_string.replace(".", "")
        date = date.replace(",", "")        #'✓ Samstag, 2. Mai, 19:05 Uhr' -->  ['✓', 'Samstag', '2', 'Mai', '19:05', 'Uhr']   len(6)
        date = date.split()                 #'✓ Morgen, 16:45 Uhr' --> ['✓', 'Morgen', '16:45', 'Uhr']   len(4)

        jetzt = time.localtime()
        jetzt_list = list(jetzt)[:-2]
        heute = datetime.datetime(*jetzt_list)

        dm = {"year":jetzt[0], "Dez":12, "Nov":11, "Okt":10, "Sep":9, "Aug":8, "Juli":7, "Juni":6, "Mai":5, "Apr":4, "Mär":3, "Feb":2,
              "Jan":1, "Tag":jetzt[2], "month":jetzt[1]}

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

    def clickElementLeadingToOwnProfile(self):
        """sucht und drückt das element das zum eigenen profil führt"""
        #self.webdriver.find_element_by_partial_link_text("Hallo").click()
        print(f"profilePathClassName: {modification.profilePathClassName()}")
        button = self.webdriver.find_element_by_class_name(modification.profilePathClassName())
        button.click()

    def extractUserIdFromUrl(self, url):
        """isoliert die fs-use-id aus der profile-url"""
        return url.split("/")[-1]

    def goToPersonalInformations(self):
        """sucht auf der hauptseite den link der zum eigenen profil führt und drückt ihn,
        wartet bis entsprechende seite geladen ist"""
        self.getSiteByUrl(self.fs_dashbord_url)

        self.clickElementLeadingToOwnProfile()
        self.waitForNextWebsite(self.fs_dashbord_url)
        return self.webdriver.current_url

    def waitForNextWebsite(self, actual_url):
        """pausiert das programm bis die nächste angeforderte seite geladen ist"""
        while actual_url == self.webdriver.current_url:
            time.sleep(0.1)
        self.actual_url = self.webdriver.current_url

    def waitForDemandedWebsite(self, demanded_website):
        "wartet darauf bis gewünschte seite geladen ist pausiert das programm bis dahin"
        while self.webdriver.current_url != demanded_website:
            time.sleep(0.1)
        self.actual_url = self.webdriver.current_url

    def clickButtonByLinkText(self, link_text):
        """sucht button auf der seite anhand des linktextes und drückt ihn"""
        button = self.webdriver.find_element_by_partial_link_text(link_text)
        button.click()

    def fsUrlByProfileIdy(self, id=315541):
        """läd eine fs Profilseite anhand der fs-nutzere-id"""
        return f"{modification.fsBaseUrl()}{modification.profileSnipet()}{id}"



    def registerNewProgrammUserAsSebFriend(self):
        """geht auf mein Profil und klickt "ich kenne" also eine "Freundschaftsanfrage" """
        if self.programm_used_first_time:
            self.getSiteByUrl(self.fsUrlByProfileIdy())
            try:
                self.clickButtonByLinkText(modification.linkTextICHKENNE())
                print("Als Nutzer des Programms registriert")
            except Exception as e:
                print(f"{Fore.RED}ERROR #09oiökwerpu --> Konnte programm nicht registrieren {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
            #self.webdriver.close()

    def getSiteByUrl(self, url):
        """fordert webdrifer auf seite mit gewünschter url zu laden
        und wartet bis entsprechende seite die aktuelle seite ist"""
        print(f"Url in getSiteByUrl() angefordert: {url}")
        self.webdriver.get(url)
        self.waitForDemandedWebsite(demanded_website=url)

    def logingIn(self, login_name, password):
        """
        logs in at foodsharing.de
        """
        self.getSiteByUrl(modification.fsBaseUrl())
        self.webdriver.find_element_by_id(modification.loginEmailLable()).send_keys(login_name)
        self.webdriver.find_element_by_id(modification.loginPasswordLable()).send_keys(password)
        self.webdriver.find_element_by_class_name(modification.loginSubmitButton()).click()
        self.waitForNextWebsite(modification.fsBaseUrl())

        print(f"Erfolgreich eingeloggt")
        return f"Erfolgreich eingeloggt"


    def runCompleteJob(self, login_name, password):
        """
        kompletter durchlauf des scraping vorgangs
        :return:
        """
        print(f"automated run step 1")
        self.logingIn(login_name, password)
        print(f"automated run step 2")
        self.registerNewProgrammUserAsSebFriend()
        print(f"automated run step 3")
        self.personal_informations_url = self.goToPersonalInformations()
        print(f"automated run step 4")
        dates, companys, urls = self.gatherTimesCompanysAndCompanySiteUrlsFromPersonalProfilSite()
        print(f"automated run step 5")
        isodates = [self.isoDateFromDateString(date) for date in dates]
        print(f"automated run step 6")
        print(f"isodates: {isodates}")
        companys_to_urls_mapping = {company:url for company, url in zip(companys, urls)}
        print(f"automated run step 7")
        print(f"{self.f}companys_to_urls_maping: {companys_to_urls_mapping} {Fore.RESET}")

        companys_to_address_mapping = {company:self.getCompanyAdressFromUrl(url) for company, url in companys_to_urls_mapping.items()}
        print(companys_to_address_mapping)
        companys_to_address_mapping = self.makeAdressMappingReadable(companys_to_address_mapping)
        print(f"{self.f}address_mapping {companys_to_address_mapping} {Fore.RESET}")

        print(f"automated run step 8")
        all_events = self.createEvents(isodates, companys, companys_to_address_mapping)
        print(f"{self.f}all_events: {all_events} {Fore.RESET}")
        self.closeBrowsdr()
        return all_events


    def createEvents(self, isodates, companys, companys_to_address_mapping, duration=modification.standardDuration()):
        all_events = []
        for isodate, company in zip(isodates, companys):
            event_here = google_tools.Event(start=isodate, duration=duration, company_name=company,
                                            location=companys_to_address_mapping[company])
            all_events.append(event_here)
        return all_events

    def makeAdressMappingReadable(self, companys_to_address_mapping:dict):
        return {company: address[8:] for company, address in companys_to_address_mapping.items()}


if __name__ == "__main__":
    modification.email()
    modification.psd()

    # test1 = fs_site_scraper.CrossPlatformJS_Driver()
    # webdriver = fs_site_scraper.CrossPlatformJS_Driver()
    # webdriver2 = fs_site_scraper.CrossPlatformJS_Driver(debug=False)

    scraper = JsFoodsharingSiteScraper(login_name=modification.email(), password=modification.psd(),
                                                       programm_used_first_time=False,
                                                       run_automated=True)

    print(f"erreicht")





