class Application:
    users_count = None
    key_count = None
    version = None
    customer_panel = None
    online_users = None
    
    def __str__(self):
        return "users=%s; keys=%s; version=%s; customer_panel=%s; online=%s" % (
            self.users_count,
            self.key_count,
            self.version,
            self.online_users,
            self.online_users
        )
        
class User:
    username = None
    ip = None
    hwid = None
    expires = None
    creation_date = None
    last_login = None
    subscription = None
    subscriptions = None
    
    def __str__(self):
        return "username=%s; ip=%s; hwid=%s; expires=%s; creation=%s; last_login=%s; subscription=%s; subscriptions=%s" % (
            self.username,
            self.ip,
            self.hwid,
            self.expires,
            self.creation_date,
            self.last_login,
            self.subscription,
            self.subscriptions
        )