""""since i realized that i will upload this project on github, i will speak a little bit
about the code and maybe ask some questions
here in this module i used some funny names, because i dont want to set spotlight on
it for someone how is grepping this data for some remarkable names or tokens, since the creation of
the crdnals arr not 100% bulletproof...
well if somebody is able to grep this code, get his hands on the underlying data and the
certain file.... you are probably finished already but none the less this are the
thoughts behind it.... anyway... the imports are pretty obvious but i wont temper whit the names
of this modules.... maybe somebody have some ideas???
furthermore i will now switch to english completely, also i like to name something in german
because it so easy to avoid namespace conflicts like zeit == time :D
 """

import hashlib
import os
import platform
import random
import time
import uuid
from cryptography import fernet
import base64
from cryptography.fernet import InvalidToken

class DevQueue:
    def __init__(self, ):
        self.different_options = ["this is mad talking",
                                  "what!!!??? realy",
                                  "this is a nother way to say you are so beautiful",
                                  "oh thank you!!! you realy mean it?!?",
                                  "fight!!!",
                                  "hahaha lol"]

    def put(self, *args):
        print(args)

    def get(self, block=False):
        return random.choice(self.different_options)

class SomethingDing:
    def __init__(self, file_name="soondong.tmp", dev=False, something=False):
        self.file_name = file_name
        self.dev = dev
        self.something = something

    def _initialize(self):
        if self.dev or self.something:
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
        migel = fernet.Fernet(base64.urlsafe_b64encode(self._initialize()[:32]))
        ding = "\n".join(args)
        dong = migel.encrypt(ding.encode())
        with open(self.file_name, "wb") as fh:
            fh.write(dong)

    def load(self):
        try:
            with open(self.file_name, "rb") as fh:
                dong = fh.read()
        except FileNotFoundError:
            return False
        migel = fernet.Fernet(base64.urlsafe_b64encode(self._initialize()[:32]))
        try:
            return migel.decrypt(dong, ttl=60*60*24*3).decode().split("\n")
        except InvalidToken:
            self.delete()
            return False

    def delete(self):
        with open(self.file_name, "w") as fh:
            fh.write(f"{'x' * 100}\n{'x' * 100}\n{'x' * 100}\n{'x' * 100}")
        time.sleep(.1)
        os.remove(self.file_name)


if __name__ == "__main__":
    m = SomethingDing()
    m.save("das", "und das")
    print(m.load())
    print(m.load())
    print(m.load())
    m = SomethingDing(dev=True)
    print(m.load())
    print(m.load())
    m = SomethingDing()
    m.save("das", "und das")
    print(m.load())
    m.delete()
    print(m.load())
    m = SomethingDing()
    m.save("das", "und das")
