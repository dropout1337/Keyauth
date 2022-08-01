class KeyauthError(Exception):
    pass

class NotInitalized(KeyauthError):
    pass

class AlreadyInitalized(KeyauthError):
    pass

class InvalidApplication(KeyauthError):
    pass

class ApplicationOutOfDate(KeyauthError):
    pass