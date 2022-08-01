
---------------------------------------
  
<br/>
<div align="center">
  <a href="https://github.com/dropout1337/Keyauth">
    <img src="https://cdn.keyauth.uk/front/assets/img/favicon.png" alt="Logo" width="120" height="120">
  </a>
  
  <h2 align="center">Keyauth API Wrapper</h3>

  <p align="center">
    KeyAuth is an Open-source authentication system with cloud-hosted subscriptions available as well.
    <br />
    <br />
    <a href="https://github.com/dropout1337/Telegram-AdBot/issues">Report Bug</a>
    ·
    <a href="https://github.com/dropout1337/Telegram-AdBot/issues">Request Feature</a>
  </p>
</div>

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
    file_hash=misc.get_checksum()
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