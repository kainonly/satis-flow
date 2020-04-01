import configparser


class Config:
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('config.ini')
        self.external_url = parser['external']['url']
        self.access_key_id = parser['oss']['access_key_id']
        self.access_key_secret = parser['oss']['access_key_secret']
        self.endpoint = parser['oss']['endpoint']
        self.bucket_name = parser['oss']['bucket_name']
