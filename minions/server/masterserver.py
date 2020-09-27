from flask import Flask, request
import requests
import os
import threading
import time
import json
from shutil import copyfile
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


MINION_SERVER_PATH = r'C:\temp\minions\minions\minionserver\minionserver.py'
PSEXEC = r'C:\temp\minions\minions\minionserver\psexec.exe'
REMOTE_PYTHON_PATH = r'c:\Users\OMER-TEST\AppData\Local\Programs\Python\Python35\python.exe'
minion_main = "print('hello word')"


def server(host='localhost', port=8000):
    app.run(host, port, debug=True)


@app.route('/')
def hello_world():
    return "<h1>Hello, I'm the master of all servers!</h1>"


@app.route('/minions', methods=['POST'])
def set_minions():
    data = request.json
    return master_server(data)


@app.route('/reminions', methods=['POST'])
def reset_minions():
    with open("cache\\cachemaster\\master.txt", "r") as file:
        data = json.load(file)
    return master_server(data)


def master_server(data):
    minions = data["config"]
    hashed_password = data["hashed_password"]
    set_up_minions(minions)
    cracking(minions, hashed_password)
    res = ever_ending_search(minions, hashed_password)
    return {"password": res}


def ever_ending_search(minions, hashed_password):
    os.system("mkdir cache\\cachemaster")
    working_minions = 0
    for minion_name in minions:
        minion = minions[minion_name]
        if minion["state"] == "searching" or minion["state"] == "done":
            working_minions += 1
    while working_minions:
        for minion_name in minions:
            minion = minions[minion_name]
            # finished search
            if minion["state"] == "done":
                minion["state"] == "done for good"
                if minion["reasult"] != "not found":
                    return minion["reasult"]
                working_minions -= 1
            # mid search
            if minion["state"] == "searching":
                try:
                    minion["from"] = int(requests.get(url="http://" + minion["host"] + ":" +
                                                      minion["port"] + "/from", json={"minion name": minion_name}).json()["from"])
                # the server has fallan and need to restart
                except:
                    minion["state"] = "down"
                    set_up_minion(minion)
                    initiate_search(minion, hashed_password, minion_name)
        # save our current state every 10 sec
        time.sleep(10)
        with open("cache\\cachemaster\\master.txt", "w") as file:
            json.dump(
                {"config": minions, "hashed_password": hashed_password}, file)
        # os.system('echo "' + data +
        #          '" > cache\\cachemaster\\master.txt')
    return "not found"


def cracking(minions, hashed_password):
    for minion_name in minions:
        minion = minions[minion_name]
        initiate_search(minion, hashed_password, minion_name)


def initiate_search(minion, hashed_password, minion_name):
    try:
        threading.Thread(
            target=minion_thread, args=(minion, hashed_password, minion_name, )).start()
    except:
        minion["state"] = "error"


def minion_thread(minion, hashed_password, minion_name):
    minion["state"] = "searching"
    minion["reasult"] = requests.get(url="http://" + minion["host"] + ":" +
                                     minion["port"] + "/crack", json={"hashed password": hashed_password, "from": minion["from"], "to": minion["to"], "minion name": minion_name}).json()["password"]
    minion["state"] = "done"


def set_up_minions(minions):
    for minion_name in minions:
        minion = minions[minion_name]
        set_up_minion(minion)

    working_minions = 0
    for minion_name in minions:
        minion = minions[minion_name]
        if minion["state"] == "up":
            working_minions += 1
    i = 0
    for minion_name in minions:
        minion = minions[minion_name]
        if minion["state"] == "up":
            minion = minions[minion_name]
            minion["from"] = 99999999//working_minions * i
            i += 1
            minion["to"] = 99999999//working_minions * i


def set_up_minion(minion):
    try:
        if minion["state"] != "up" and minion["state"] != "searching":
            print('aaaaa')
            connection = MinionSetupWindowsConnecor(minion["host"])
            print('aaaaa')

            connection.connect(minion["user"], minion["password"])

            # copying minionserver.py
            connection.upload(MINION_SERVER_PATH)
            
            connection.run()
    # running server
        # os.system("python -m minions.minionserver run-server -h " +
        #             minion["host"] + " -p " + minion["port"])
        # # if it's not on the same machine
        # if minion["ip"] != "localhost":
        #     os.chdir('C:')
        #     # closing connection
        #     os.system("net use p: /delete")
    except:
        minion["state"] = "error"

class MinionSetupWindowsConnecor:
    def __init__(self, host):
        self.host = host
        self.temp_dir = ''


    def connect(self, user, pswd):
        print(r'net use  \\%s\C$ %s /user:%s' % (self.host, pswd, user))
        print(r'net use  \\%s\IPC$ %s /user:%s' % (self.host, pswd, user))
        os.system(r'net use  \\%s\C$ %s /user:%s' % (self.host, pswd, user))
        self.temp_dir = r'\\%s\C$\temp' % (self.host, )
        os.system('mkdir ' + self.temp_dir)

    
    def disconnect(self):
        os.system(r"net use \\%s\IPC$ /delete" % (self.host))
        os.system(r"net use \\%s\C$ /delete" % (self.host))

    def upload(self, local_path):
        os.system('copy ' + local_path + ' '+  self.temp_dir + "\\" + os.path.basename(local_path))

    def run(self):
        os.system(r'%s /S \\%s -i %s' % (PSEXEC, self.host, REMOTE_PYTHON_PATH))
 
if __name__ == "__main__":
    # set_up_minion({
    #     'user': 'Administrator',
    #     'password': 'Password1!',
    #     'host': 'omer-test-pc'
    # })
    server()