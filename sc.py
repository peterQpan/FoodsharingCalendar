import base64
import hashlib
import os
import platform
import time
import uuid

import fernet as fernet
from pip._vendor.colorama import Fore


class SomethingDing:
    def __init__(self, file_name="soondong.tmp", debug=False, something:str=False):
        self.file_name = file_name
        self.debug = debug
        self.something = something

    def _initialize(self):
        if self.debug or self.something:
            a =77748881999
        else:
            a = uuid.getnode()
        b= ""
        for x in platform.uname():
            b += str(x)
        if self.something:
            return hashlib.pbkdf2_hmac("sha1", self.something.encode(), str(a).encode(), 200, dklen=32)
        return hashlib.pbkdf2_hmac("sha1", b.encode(), str(a).encode(), 200, dklen=32)

    def save(self, *args):
        print(f"#02398723ß SomethingDing.save: {args}")
        migel = fernet.Fernet(base64.urlsafe_b64encode(self._initialize()[:32]))
        ding = "\n".join(args)
        dong = migel.encrypt(ding.encode())
        with open(self.file_name, "wb") as fh:
            fh.write(dong)

    def load(self):
        try:
            with open(self.file_name, "rb") as fh:
                dong = fh.read()
        except FileNotFoundError as e:
            print(f"{Fore.RED}ERROR #kas09u23ojbk23 --> keine zugangsdaten gespeichert {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")

            return False
        migel = fernet.Fernet(base64.urlsafe_b64encode(self._initialize()[:32]))
        try:
            return migel.decrypt(dong, ttl=60*60*24*3).decode().split("\n")
        except fernet.InvalidToken as e:
            print(f"{Fore.RED}ERROR #90304ij2o3 -->  {e.__traceback__.tb_lineno}, {repr(e.__traceback__)}, {repr(e)},  {e.__cause__}{Fore.RESET}")

            self.delete()
            return False

    def delete(self):
        with open(self.file_name, "w") as fh:
            fh.write(f"{'x' * 100}\n{'x' * 100}\n{'x' * 100}\n{'x' * 100}")
        time.sleep(.1)
        os.remove(self.file_name)


def saveCredentialsToSecureFile(input_file_path=r"/home/ich/PycharmProjects/foodcalendar/credentials.json",
                                output_file_path=r"/home/ich/PycharmProjects/foodcalendar/crs.scr",
                                something="2lksölkjasiuioalkasd9ß0ü9uiöoknöknaskjhhjg"):
    with open(input_file_path) as in_fh:
        content = in_fh.read()
    sc_tool = SomethingDing(output_file_path, something=something)
    sc_tool.save(content)


def saveFsLoginData(email, psd, save_file_name="soondong.tmp"):
    print(f"#92876832 saveLoginData")
    sc_tool = SomethingDing(save_file_name)
    sc_tool.save(email, psd)

def loadLoginData(save_file_name="soondong.tmp"):
    sc_tool = SomethingDing(save_file_name)
    return sc_tool.load()

if __name__ == '__main__':
    email = "peTerfrOst1713@gmail.com"
    psd = "lakjnsad09uwiihl2ijnldfkjnjhbk.jsiuh8ewuoilqnkjbdhjbfsdoivhjoiuhiluh4ljbkl1b23knbbsd"
    saveFsLoginData(email=email, psd=psd)
    time.sleep(1)
    new_email, new_psd = loadLoginData()
    print(f"1. {email == new_email}, 2. {psd == new_psd}")

    #saveCredentialsToSecureFile()





