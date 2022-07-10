from . import *
import selenium
class Handling():
    def __init__(self,e, version):
        if isinstance(e, selenium.common.exceptions.WebDriverException):
            raise DriverError("Your chrome/chromium version is lower than {0} or chrome/chromium is not installed, to avoid errors install version {0}, or higher".format(version))