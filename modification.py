import os

import PySimpleGUI as sg


# todo hier gehts weiter: hier schon int zu machen gibt in der popup version int.replace error
def loadUserConfigurations(file_name="modifications.ini"):
    user_configs = {}
    with open(file_name) as fh:
        for line in fh.readlines():
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            key, split, value = line.partition(" ")
            try:
                user_configs[key] = value
            except Exception as e:
                sg.Print(f"Fehler beim Versuch key={key} : value={value} ins Dictionary zu schreiben")
    return user_configs


def fsBaseUrl():
    return 'https://foodsharing.de/'


def fsDashbordPostfix():
    return '?page=dashboard'


def loginEmailLable():
    """java script element name für email feld"""
    return "login-email"


def loginPasswordLable():
    """java script element name für password feld"""
    return "login-password"


def loginSubmitButton():
    """java script element name für login ok button"""
    return "btn.btn-secondary.btn-sm"


def linkTextICHKENNE():
    """genauer linktext des javy script links-buttons der gedrückt werden soll"""
    return "ich kenne"


def profilePathClassName():
    return "avatar.size-50.sleepmode-0"


def profileSnipet():
    return "profile/"


def integerTupleFromUserInput(input_kind):
    minutes = user_configs.get(input_kind, "")
    try:
        return (int(minutes),)
    except:
        if minutes:
            try:
                minutes = minutes.replace(" ", "")
                return tuple(int(x) for x in minutes.split(","))
            except:
                sg.Print(f"Fehler beim Versuch die werte von {input_kind}={minutes} zu holen")
        else:
            return ()


def popupMinutes():
    return integerTupleFromUserInput("popup_minutes")


def emailMinutes():
    return integerTupleFromUserInput("email_minutes")


def color_id():
    """farb_id von 0-11
    1: flieder, 2 hellgrün, 3 lila, 4 orange, 5 gelb, 6 rot-orange, 7 hellblau, 8 grau, 9 blau, 10 grün, 11 rot
    """
    return int(user_configs.get("color_id", 0))


def calendar_id():
    return user_configs.get("calendar_id", "primary")


def programmUsedFirst():
    """
    checks if there is an already self created file
    and determines from this if program is used the first time
    :return: bool
    """
    if os.path.exists(os.path.join(".", "soondong.tmp")):
        return False
    return True


def debug():
    return True


def simpleInitUserConf(input_type, defalult):
    try:
        return int(user_configs.get(input_type, defalult))
    except:
        sg.Print(f"Fehler beim Versuch die werte von {user_configs[input_type]} in integer zu wandeln")


def timeBoundery():
    return simpleInitUserConf("timeBoundery", 45)


def standardDuration():
    return simpleInitUserConf("standardDuration", 45)


def firsWindowSize():
    return (80, 28)


def firstWindowFontSize():
    return ("Standard", 10)


def companyAdressElementId():
    return "inputAdress"


def companyAdressElementClassName():
    return "ui-widget.ui-widget-content.corner-bottom.margin-bottom.ui-padding"


user_configs = loadUserConfigurations("modifications.ini")


def dateAndCompanyListKey():
    return "clear.datelist"
