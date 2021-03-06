import configparser
import requests
import hashlib
import sys

client = None


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def cracking_password(self, path, hashed_password):
        config = configparser.ConfigParser()
        config.read(path)
        # data = {"hashed_password": hashlib.md5(hashed_password.encode()).hexdigest(), "config": config._sections}
        data = {"hashed_password": hashed_password, "config": config._sections}
        print(requests.post(url="http://" + self.host + ":" + str(self.port) + "/minions", json=data).json())

    def reset_master(self):
        print(requests.post(url="http://" + self.host + ":" + str(self.port) + "/reminions").json())


def upload_config(host, port, hashedpassword, path):
    client = Client(host, port)
    client.cracking_password(path, hashedpassword)


def reset_server(host, port):
    client = Client(host, port)
    client.reset_master()
