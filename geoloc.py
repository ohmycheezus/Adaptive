import ipinfo
import os

class Locator:
    def __init__(self):
        self.token = os.environ.get('IPINFO')
        self.handler = ipinfo.getHandler(self.token)
        self.details = self.handler.getDetails()
    def autolocation(self):
        return f'{self.details.city}, {self.details.country}'
