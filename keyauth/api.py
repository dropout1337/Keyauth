import os
import binascii
import requests
from json import loads
from uuid import uuid4
from Crypto.Hash import SHA256

from .exceptions import *
from .classes import *
from .misc import misc
from .encryption import encryption

class Keyauth():
    
    def __init__(self, name: str, owner_id: str, secret: str, version: str, file_hash: str):
        self.session = requests.Session()
        self.base_url = "https://keyauth.win/api/1.0/"
    
        self._name = name
        self._owner_id = owner_id
        self._secret = secret
        self._version = version
        self._hash = file_hash
        
        self._session_id = None
        self._initialized = False
        
        self._encrypt_key = None
        
        self._init_iv = lambda: SHA256.new(str(uuid4())[:8].encode()).hexdigest()
        
        self.user = User()
        self.application = Application()
        
        self.init()
        
    def _load_application(self, data: dict):
        self.application.users_count = data["numUsers"]
        self.application.key_count = data["numKeys"]
        self.application.version = data["version"]
        self.application.customer_panel = data["customerPanelLink"]
        self.application.online_users = data["numOnlineUsers"]
    
    def _load_user(self, data: dict):
        self.user.username = data["username"]
        self.user.ip = data["ip"]
        self.user.hwid = data["hwid"]
        self.user.expires = data["subscriptions"][0]["expiry"]
        self.user.creation_date = data["createdate"]
        self.user.last_login = data["lastlogin"]
        self.user.subscription = data["subscriptions"][0]["subscription"]
        self.user.subscriptions = data["subscriptions"]

    def init(self):
        if self._session_id != None:
            raise AlreadyInitalized(
                "You've already initialized..."
            )
        
        init_iv = self._init_iv()
        self._encrypt_key = SHA256.new(str(uuid4())[:8].encode()).hexdigest()
        
        payload = {
            "type": binascii.hexlify(("init").encode()),
            "ver": encryption.encrypt(self._version, self._secret, init_iv),
            "hash": self._hash,
            "enckey": encryption.encrypt(self._encrypt_key, self._secret, init_iv),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        if response == "KeyAuth_Invalid":
            raise InvalidApplication("The application doesn't exist.")
        else:
            response = encryption.decrypt(response, self._secret, init_iv)
            json = loads(response)
        
        if json["message"] == "invalidver":
            if json["download"] != "":
                raise ApplicationOutOfDate(json["download"])
            else:
                raise ApplicationOutOfDate("Invalid version.")
        
        if not json["success"]:
            raise KeyauthError(json["message"])
        
        self._session_id = json["sessionid"]
        self._initialized = True
        
        self._load_application(json["appinfo"])
        
    def register(self, username: str, password: str, license_key: str, hwid: str = None):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        if hwid == None: hwid = misc.get_hwid()
        init_iv = self._init_iv()
        
        payload = {
            "type": binascii.hexlify(("register").encode()),
            "username": encryption.encrypt(username, self._encrypt_key, init_iv),
            "pass": encryption.encrypt(password, self._encrypt_key, init_iv),
            "key": encryption.encrypt(license_key, self._encrypt_key, init_iv),
            "hwid": encryption.encrypt(hwid, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)
        
        if json["success"]:
            self._load_user(json["info"])
            return True
        else:
            raise KeyauthError(json["message"])

    def upgrade(self, username: str, license_key: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()
        
        payload = {
            "type": binascii.hexlify(("upgrade").encode()),
            "username": encryption.encrypt(username, self._encrypt_key, init_iv),
            "key": encryption.encrypt(license_key, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)
        
        if json["success"]:
            return True
        else:
            raise KeyauthError(json["message"])

    def login(self, username: str, password: str, hwid: str = None):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        if hwid == None: hwid = misc.get_hwid()
        init_iv = self._init_iv()
        
        payload = {
            "type": binascii.hexlify(("login").encode()),
            "username": encryption.encrypt(username, self._encrypt_key, init_iv),
            "pass": encryption.encrypt(password, self._encrypt_key, init_iv),
            "hwid": encryption.encrypt(hwid, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)
        
        if json["success"]:
            self._load_user(json["info"])
            return True
        else:
            raise KeyauthError(json["message"])
        
    def license(self, license_key: str, hwid: str = None):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        if hwid == None: hwid = misc.get_hwid()
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("license").encode()),
            "key": encryption.encrypt(license_key, self._encrypt_key, init_iv),
            "hwid": encryption.encrypt(hwid, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            self._load_user(json["info"])
            return True
        else:
            raise KeyauthError(json["message"])

    def var(self, name: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("var").encode()),
            "varid": encryption.encrypt(name, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return json["message"]
        else:
            raise KeyauthError(json["message"])

    def getvar(self, var_name: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("getvar").encode()),
            "var": encryption.encrypt(var_name, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return json["response"]
        else:
            raise KeyauthError(json["message"])

    def setvar(self, var_name: str, var_data: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("setvar").encode()),
            "var": encryption.encrypt(var_name, self._encrypt_key, init_iv),
            "data": encryption.encrypt(var_data, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return True
        else:
            raise KeyauthError(json["message"])

    def ban(self):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("ban").encode()),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return True
        else:
            raise KeyauthError(json["message"])

    def file(self, file_id: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("file").encode()),
            "fileid": encryption.encrypt(file_id, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if not json["success"]: raise KeyauthError(json["message"])
        return binascii.unhexlify(json["contents"])

    def webhook(self, webid: str, param: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("webhook").encode()),
            "webid": encryption.encrypt(webid, self._encrypt_key, init_iv),
            "params": encryption.encrypt(param, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return json["message"]
        else:
            raise KeyauthError(json["message"])

    def check(self):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("check").encode()),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return True
        else:
            return False

    def check_blacklist(self):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()
        hwid = misc.get_hwid()

        payload = {
            "type": binascii.hexlify(("checkblacklist").encode()),
            "hwid": encryption.encrypt(hwid, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        response = self.session.post(self.base_url, data=payload).text
        response = encryption.decrypt(response, self._encrypt_key, init_iv)
        json = loads(response)

        if json["success"]:
            return True
        else:
            return False

    def log(self, message: str):
        if self._initialized == False: raise NotInitalized("You have not initialized this session.")
        init_iv = self._init_iv()

        payload = {
            "type": binascii.hexlify(("log").encode()),
            "pcuser": encryption.encrypt(os.getenv("username"), self._encrypt_key, init_iv),
            "message": encryption.encrypt(message, self._encrypt_key, init_iv),
            "sessionid": binascii.hexlify(self._session_id.encode()),
            "name": binascii.hexlify(self._name.encode()),
            "ownerid": binascii.hexlify(self._owner_id.encode()),
            "init_iv": init_iv
        }
        
        self.session.post(self.base_url, data=payload)