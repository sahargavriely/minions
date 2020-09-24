import configparser
import requests


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def setting_up_minions(self, path):
        config = configparser.ConfigParser()
        config.read(path)

        # TO DO
        # check if the data is in the right format

        requests.post(url="http://" + self.host + ":" +
                      str(self.port) + "/minions", json=config._sections)

    def cracking_password(self, hashed_password):

        # TO DO
        # check if the data is in the right format

        requests.post(url="http://" + self.host + ":" + str(self.port) +
                      "/crack", json={"hashed_password": hashed_password})


def upload_config(host, port, path):
    client = Client(host, port)
    client.setting_up_minions(path)


def crack_password(hashed_password):
    if client:
        client.cracking_password(hashed_password)
    else:
        print("Please upload configuration first")


client = None
