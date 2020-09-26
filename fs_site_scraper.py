import datetime
import os
import pickle
import platform
import queue
import re
import sys
import threading
import time

import selenium.webdriver.firefox.options
from PySimpleGUI import Print
from pip._vendor.colorama import Fore
from selenium import webdriver

import email_and_psd
import google_tools
import modification
import tools


class UnknownOS(Exception):
    pass


class CrossPlatformJS_Driver(webdriver.Firefox):
    def __init__(self, debug=modification.debug()):  # super() wird in den funktionen gerufen
        self.f = Fore.MAGENTA
        print(f"#09ui {self.f}{self.__class__.__name__} geladen {Fore.RESET}")

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
            Print("#897uoin Apple?!? Pech!!! :P")
            time.sleep(sys.maxsize)
            sys.exit(666)
        else:
            raise UnknownOS

    def loadRightDriverByBrutforce(self, path_string, options):

        drivers = sorted(os.listdir(path_string), reverse=True)

        for driver_file_name in drivers:
            driver_file_path = os.path.join(path_string, driver_file_name)
            try:
                print(f"#98zihknm {self.f}geladen werden soll: {driver_file_path} {Fore.RESET}")
                super().__init__(executable_path=driver_file_path, options=options)
                print(f"#9872u3n {self.f}geladen wurde: {driver_file_path} {Fore.RESET}")
                return
            except Exception as e:
                print(f"#0998iuh2gff2 {Fore.RED}ERROR #09kölkweröklqw --> Treiber laden fehlgeschlagen {e.__traceback__.tb_lineno}, "
                      f"{repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
                Print("Webbrowser-Driver fehlgeschlagen, existiert der Geckodriver im richtigen Pfad?!? ---> README")


class BaseSiteScraper:

    def __init__(self, login_name, password, debug):
        if login_name and password:
            self.initiateWebdriver(debug=debug)
            
            self.logingIn(login_name=login_name, password=password)


    def initiateWebdriver(self, debug):
        self.webdriver = CrossPlatformJS_Driver(debug=debug)

    def waitForNextWebsite(self, old_url, max_count = 150):
        """pausiert das programm bis die nächste angeforderte seite geladen ist
        :return next_website_url"""
        while self.webdriver.current_url == old_url and max_count > 0:
            print(f"#6767676 ausgelöst: {max_count}, current url: {self.webdriver.current_url}, old url: {old_url}")
            max_count -= 1
            time.sleep(0.2)
        print(f"#123123 verlassen mit: {max_count} old url: {old_url}, current url: {self.webdriver.current_url}")

        if max_count == 0:
            print(f"#4343434 ausgelö0t: {True}")
            return

        self.actual_url = self.webdriver.current_url
        print(f"#93939393 actual_url: {self.actual_url}")
        return self.actual_url

    def waitForDemandedWebsite(self, demanded_website):
        "wartet darauf bis gewünschte seite geladen ist pausiert das programm bis dahin"
        while self.webdriver.current_url != demanded_website:
            time.sleep(0.1)
        self.actual_url = self.webdriver.current_url


    def getSiteByUrl(self, url):
        """fordert webdrifer auf seite mit gewünschter url zu laden
        und wartet bis entsprechende seite die aktuelle seite ist"""
        # print(f"#lkkjhas89732 Url in getSiteByUrl() angefordert: {url}")
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
        print(f"#lkasjdlfk Erfolgreich eingeloggt")
        return f"Erfolgreich eingeloggt"

    def closeBrowser(self):
        # self.webdriver.close()
        pass

    def clickButtonByLinkText(self, link_text):
        """sucht button auf der seite anhand des linktextes und drückt ihn"""
        button = self.webdriver.find_element_by_partial_link_text(link_text)
        button.click()




class AutomatedFSDateSiteScraper(BaseSiteScraper):
    # No error handeling, its better to crash, than do something wrong when creating
    # Events, furthermore Events with google.location with route

    def __init__(self, login_name, password, programm_used_first_time, run_automated=True, debug=modification.debug()):

        super(AutomatedFSDateSiteScraper, self).__init__(login_name=login_name, password=password, debug=debug)
        self.f = Fore.CYAN

        self.programm_used_first_time = programm_used_first_time
        self.personal_informations_url = None
        self.actual_url = None
        self._events = None

        self.dates = []
        self.companys = []
        self.addresses = []

        print(f"#870293uijkna {self.f}{self.__class__.__name__} geladen {Fore.RESET}")

        if run_automated:
            self.all_events = self.runCompleteJob(login_name, password)

    @property
    def fs_dashboard_url(self):
        return f"{modification.fsBaseUrl()}{modification.fsDashbordPostfix()}"

    @property
    def profile_id(self):
        try:
            return self.personal_informations_url.split("/")[-1]
        except Exception as e:
            print(f"#lkkhasjlk {Fore.RED}ERROR #90uo43öljknwer -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, "
                  f"{repr(e)},  {e.__cause__}{Fore.RESET}")
            print(f"#lkjaksd {self.f}Es steht noch keine Informationen über die Nutzer_Id bereit {Fore.RESET}")

    def allFsEvents(self):
        return self.all_events


    def gatherTimesCompanysAndCompanySiteUrlsFromPersonalProfilSite(self):
        """sammelt abhol_datums, betriebs namen, und betriebs_seite_urls

        :return: abhol_dates, companies, urls
        """
        self.getSiteByUrl(self.personal_informations_url)

        content_box = self.webdriver.find_element_by_class_name(modification.dateAndCompanyListKey())
        date_company_link_snipets = content_box.find_elements_by_tag_name("a")
        assert len(date_company_link_snipets) % 2 == 0

        abhol_dates = [x.text for i, x in enumerate(date_company_link_snipets) if i % 2 == 0]
        companies = [x.text for i, x in enumerate(date_company_link_snipets) if i % 2 == 1]
        urls = [f"{snipet.get_attribute('href')}" for i, snipet in enumerate(date_company_link_snipets) if i % 2 == 1]

        print(f"#98auih {self.f}links: {urls}\ndates: {abhol_dates}\ncompanys: {companies}{Fore.RESET}")
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
                print(f"#298i32 in getCompanyAdresse from url, ausgabe: {adress_block.text}")
                return adress_block.text
            except:
                time.sleep(0.01)

    def isoDateFromDateString(self, date_string):  # datetime.datetime
        """
        wandelt den datestring der aus der webseite gezogen wird vollautomatisch in eine vergleichbare und
        per timedelta veränderbares "iso_date" eine datetime.datetime() um

        :param date_string: z.B. '✓ Samstag, 2. Mai, 19:05 Uhr' oder '✓ Morgen, 16:45 Uhr'
        :return: datetime.datetime(2020, 5, 1, 16, 45)
        """
        # todo modularize this here!!!
        date = date_string.replace(".", "")
        date = date.replace(",",
                            "")  # '✓ Samstag, 2. Mai, 19:05 Uhr' -->  ['✓', 'Samstag', '2', 'Mai', '19:05', 'Uhr']   len(6)
        date = date.split()  # '✓ Morgen, 16:45 Uhr' --> ['✓', 'Morgen', '16:45', 'Uhr']   len(4)

        jetzt = time.localtime()
        jetzt_list = list(jetzt)[:-2]
        heute = datetime.datetime(*jetzt_list)

        dm = {"year": jetzt[0], "Dez": 12, "Nov": 11, "Okt": 10, "Sep": 9, "Aug": 8, "Juli": 7, "Juni": 6, "Mai": 5,
              "Apr": 4, "Mär": 3, "Feb": 2,
              "Jan": 1, "Tag": jetzt[2], "month": jetzt[1]}

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
        print(f"profilePathClassName: {modification.profilePathClassName()}")
        button = self.webdriver.find_element_by_class_name(modification.profilePathClassName())
        button.click()

    @staticmethod
    def extractUserIdFromUrl(url):
        """isoliert die fs-use-id aus der profile-url"""
        return url.split("/")[-1]

    def goToPersonalInformations(self):
        """sucht auf der hauptseite den link der zum eigenen profil führt und drückt ihn,
        wartet bis entsprechende seite geladen ist"""
        self.getSiteByUrl(self.fs_dashboard_url)

        self.clickElementLeadingToOwnProfile()
        self.waitForNextWebsite(self.fs_dashboard_url)
        return self.webdriver.current_url



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
                print(
                    f"{Fore.RED}ERROR #09oiökwerpu --> Konnte programm nicht registrieren {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")



    def runCompleteJob(self, login_name, password):
        """
        kompletter durchlauf des scraping vorgangs
        :return:
        """
        print(f"automated run step 1")
        self.registerNewProgrammUserAsSebFriend()
        print(f"automated run step 3")
        self.personal_informations_url = self.goToPersonalInformations()
        print(f"automated run step 4")
        dates, companys, urls = self.gatherTimesCompanysAndCompanySiteUrlsFromPersonalProfilSite()
        print(f"#0092323 dates: {dates}")
        print(f"#90ß0293 companys: {companys}")
        print(f"#ow02o9u urls: {urls}")
        print(f"automated run step 5")
        isodates = [self.isoDateFromDateString(date) for date in dates]
        print(f"automated run step 6")
        print(f"isodates: {isodates}")
        companys_to_urls_mapping = {company: url for company, url in zip(companys, urls)}
        print(f"automated run step 7")
        print(f"{self.f}companys_to_urls_maping: {companys_to_urls_mapping} {Fore.RESET}")

        companys_to_address_mapping = {company: self.getCompanyAdressFromUrl(url) for company, url in
                                       companys_to_urls_mapping.items()}
        print(companys_to_address_mapping)
        companys_to_address_mapping = self.makeAdressMappingReadable(companys_to_address_mapping)
        print(f"{self.f}address_mapping {companys_to_address_mapping} {Fore.RESET}")

        print(f"automated run step 8")
        all_events = self.createEvents(isodates, companys, companys_to_address_mapping)
        print(f"{self.f}all_events: {all_events} {Fore.RESET}")
        self.closeBrowser()
        return all_events

    def createEvents(self, isodates, companys, companys_to_address_mapping, duration=modification.standardDuration()):
        all_events = []
        for isodate, company in zip(isodates, companys):
            event_here = google_tools.Event(start=isodate, duration=duration, company_name=company,
                                            location=companys_to_address_mapping[company])
            all_events.append(event_here)
        return all_events

    def makeAdressMappingReadable(self, companys_to_address_mapping: dict):
        return {company: address[8:] for company, address in companys_to_address_mapping.items()}


class AllMemberScraper(BaseSiteScraper):
    def __init__(self, email=email_and_psd.email, psd=email_and_psd.psd):

        super(AllMemberScraper, self).__init__(login_name=email, password=psd, debug=True)
        self.member_container = tools.MemberContainer()

        self.float_pattern = re.compile(r'[\d]*[.][\d]+')
        self.int_pattern = re.compile(r"\d+")

    def getAllMembers(self, first_member_url="https://foodsharing.de/?page=bezirk&bid=159&sub=members"):
        """
        gets all members of a certain district, starting with the first url to the first page, and klicks
        itself next page, next page, next page and excerpts Name and url of these district members
        and sets with thes information new members in self.member_container
        :param first_member_url: url of districtt page to start with
        """
        self.webdriver.implicitly_wait(10)
        self.getSiteByUrl(first_member_url)
        while True:
            member_names, member_urls = self.getAllMembersFromActualSite()
            [self.member_container.setUser(member_url=member_url, member_name=member_name)
             for member_url, member_name in zip(member_urls, member_names)]
            if not self.clickElementLeadingToNextPage():
                break
        self.webdriver.implicitly_wait(0)


    def clickElementLeadingToNextPage(self):
        """sucht und drückt das element das zur nächsten Seite führt"""
        buttons = self.webdriver.find_elements_by_class_name("page-link")
        for button in buttons:
            if button.text == '›':
                if button.get_attribute('aria-disabled'):
                    return False
                else:
                    button.click()
                    return True



    def getAllMembersFromActualSite(self):
        member_box = self.webdriver.find_element_by_class_name("table.b-table.table-hover.table-sm")
        member_nodes = member_box.find_elements_by_tag_name("a")
        member_names = [member_node.text for member_node in member_nodes]
        member_urls = [member_node.get_attribute("href") for member_node in member_nodes]
        return member_names, member_urls


    def saveContainer(self, file_path="container.sav"):
        with open(file_path, "wb") as fh:
            pickle.dump(self.member_container, fh)
        print(f"#6672763 member_container saved: {file_path}")

    def loadContainer(self, file_path="container.sav"):
        with open(file_path, "rb") as fh:
            saved_container = pickle.load(fh)
        saved_container.update(self.member_container)
        self.member_container = saved_container
        print(f"#9872340239 member_container loaded: {file_path} members: {len(self.member_container)}")



    def __del__(self):
        if self.webdriver:
            self.webdriver.close()
            
    def getAllMemberDataFromSiteUrl(self, member_url):

        result_dict = {}
        self.getSiteByUrl(member_url)
        

        result_dict = self.getMemberDevotionData(result_dict=result_dict)

        result_dict = self.getMemberAchievementData(result_dict=result_dict)

        self.getMemberBananes(result_dict=result_dict)

        print(f"#8727882929 data for {member_url}: {result_dict}")

        return result_dict

    def getMemberBananes(self, result_dict):
        banana_lable = {"item stat_bananacount"}
        all_a_nodes = self.webdriver.find_elements_by_tag_name("a")

        for node in all_a_nodes:
            class_strig = node.get_attribute('class')
            if class_strig in banana_lable:
                value_string = node.text

                result_dict["Bananen"] = self.getAmountValue(value_string)
        return result_dict




    def getMemberAchievementData(self, result_dict):
        achievement_lables = {"item stat_fetchweight": "abgeholt", "item stat_fetchcount": "Anzahl Abholungen",
                              "item stat_postcount": "Posts erstellt", "item stat_basketcount": "Essenskörbe erstellt",
                              #"item stat_bananacount": "Bananen"
                              }
        all_span_nodes = self.webdriver.find_elements_by_tag_name("span")

        for node in all_span_nodes:
            class_name = node.get_attribute('class')
            if class_name in achievement_lables.keys():
                value_string = node.text.strip()
                result_dict[achievement_lables[class_name]] = self.getAmountValue(value_string)

        return result_dict


    def getAmountValue(self, string):
        amount_f = re.findall(self.float_pattern, string)
        if amount_f:
            try:
                return float(amount_f[0])
            except Exception as e:
                print(f"{Fore.RED}ERROR #9879778911 --> sting: {string}; amount_f: {amount_f} {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
        amount_i = re.findall(self.int_pattern, string)
        if amount_i:
            try:
                return int(amount_i[0])
            except Exception as e:
                # print(f"t} : {}")
                print(f"{Fore.RED}ERROR #98723239778911 --> sting: {string}; amount_i: {amount_i} {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")
        return 0


    def getMemberDevotionData(self, result_dict):
        devotion_attributes = {"Botschafter", "Foodsaver in", "Stammbezirk", "Ansprechpartner", "Schlafmütze"}

        all_p_nodes = self.webdriver.find_elements_by_tag_name("p")


        devotion_strings = [p_node.text for p_node in all_p_nodes if p_node.text]
        for possible_attribute in devotion_strings:
            key, values = self.confirmData(data= possible_attribute, attributes= devotion_attributes)
            if key:
                result_dict[key] = values
        return result_dict



    def confirmData(self, data, attributes):
        for attribute in attributes:
            if attribute in data:
                first, new_line, value_string = data.partition("\n")
                values = value_string.split(", ")
                return attribute, values
        return False, False
    

if __name__ == "__main__":
    pass

    # member_scraper = AllMemberScraper()
    # member_scraper.getAllMembers()
    # print(f"#ß0908998 {len(member_scraper.member_container)}")
    # print(f"#987230 {[member_scraper.member_container[member_url]['name'] for member_url in member_scraper.member_container]}")
    # member_scraper.saveContainer()



    # test1 = fs_site_scraper.CrossPlatformJS_Driver()
    # webdriver = fs_site_scraper.CrossPlatformJS_Driver()
    # webdriver2 = fs_site_scraper.CrossPlatformJS_Driver(debug=False)

    # scraper = AutomatedFSDateSiteScraper(login_name=modification.email(), password=modification.psd(),
    #                                      programm_used_first_time=False,
    #                                      run_automated=True)
    #

