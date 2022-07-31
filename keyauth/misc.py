import os
import hashlib
import platform
import win32security

class misc:

    @staticmethod
    def get_hwid():
        winuser = os.getlogin()
        if platform.system() != "Windows":
            with open("/etc/machine-id") as f:
                hwid = f.read()
                return hwid

        sid = win32security.LookupAccountName(None, winuser)[0]
        sidstr = win32security.ConvertSidToStringSid(sid)

        return sidstr
    
    @staticmethod
    def get_checksum():
        path = os.path.basename(__file__)
        if not os.path.exists(path):
            path = path[:-2] + "exe"
            
        md5_hash = hashlib.md5()
        a_file = open(path, "rb")
        content = a_file.read()
        md5_hash.update(content)
        digest = md5_hash.hexdigest()
        
        return digest
