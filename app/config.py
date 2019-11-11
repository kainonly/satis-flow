import configparser


class Config:
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        self.base_url = parser['docker']['base_url']
        self.username = parser['docker']['username']
        self.password = parser['docker']['password']
        self.registry = parser['docker']['registry']
        self.repository = parser['docker']['repository']
        self.external_url = parser['external']['url']
