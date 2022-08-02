
---------------------------------------
# Keyauth API Wrapper  
- KeyAuth is an Open-source authentication system with cloud-hosted subscriptions available as well.

---------------------------------------

# Installation
```bash
pip3 install keyauth
```

# Usage
```python
import pwinput
from keyauth import *

client = Keyauth(
    name="application name",
    owner_id="your account id",
    secret="application secret",
    version="current version",
    file_hash=None
)

print(client.application)
print("Validation status: %s" % (client.check()))
print("Blacklist status: %s" % (client.check_blacklist()))

print()

print("1=login; 2=register; 3=upgrade, 4=license key")
option = int(input("Option: "))

if option == 1:
    reply = client.login(
        username=input("Username: "),
        password=pwinput.pwinput("Password: ")
    )
if option == 2:
    reply = client.register(
        username=input("Username: "),
        password=pwinput.pwinput("Password: "),
        license_key=pwinput.pwinput("License: ")
    )
if option == 3:
    reply = client.upgrade(
        username=input("Username: "),
        license_key=pwinput.pwinput("License: ")
    )
if option == 4:
    reply = client.license(
        license_key=pwinput.pwinput("License: ")
    )

print(client.user)
```

- Please note that file hash checking isnt needed on python applications. (But you can still use if ofcourse)