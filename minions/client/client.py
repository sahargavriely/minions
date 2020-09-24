import configparser
import requests
import hashlib

client = None


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def cracking_password(self, path, hashed_password):
        config = configparser.ConfigParser()
        config.read(path)
        data = {"hashed_password": hashlib.md5(
            hashed_password.encode()).hexdigest(), "config": config._sections}
        # TO DO
        # check if the data is in the right format
        requests.post(url="http://" + self.host + ":" +
                      str(self.port) + "/minions", json=data)


def upload_config(host, port, hashedpassword, path):
    client = Client(host, port)
    client.cracking_password(path, hashedpassword)
