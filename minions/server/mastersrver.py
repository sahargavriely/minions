from flask import Flask, request
import requests
import os
import threading
import time
import json
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


minion_server = "print('hello word')"
minion_main = "print('hello word')"


def server(host, port):
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
    file = open("cache\\cachemaster\\master.txt", "r")
    data = json.loads(file.read())
    file.close()
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
        data = json.dumps(
            {"config": minions, "hashed_password": hashed_password})
        with open("cache\\cachemaster\\master.txt", "w") as file:
            file.write(data)
        os.system('echo "' + data +
                  '" > cache\\cachemaster\\master.txt')
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
    # if the minion is needed to be set-up
    if "state" not in minion or minion["state"] != "up":
        minion["state"] = "up"
        if "port" not in minion:
            minion["port"] = "8000"
        if "host" not in minion:
            minion["host"] = minion["ip"]
        try:
            # if it's not on the same machine
            if minion["ip"] != master_server["host"]:
                # getting a net use connection
                if "password" not in minion or minion["password"] == "":
                    os.system("net use p: \\\\" +
                              minion["ip"] + "\\Users\\" + minion["user"])
                else:
                    os.system("net use p: \\\\" + minion["ip"] + "\\Users\\" + minion["user"] +
                              " " + minion["password"] + " /user:" + minion["user"])
                # moving to the shared computer
                os.chdir('P:')
                os.chdir('Desktop')
                os.system("mkdir minions\\minionserver")
                # copying minionserver.py
                os.system("echo " + minion_server +
                          "> minions\\minionserver\\minionserver.py")
                # copying __main__.py
                os.system("echo " + minion_main +
                          "> minions\\minionserver\\__main__.py")
            # running server
            os.system("python -m minions.minionserver run-server -h " +
                      minion["host"] + " -p " + minion["port"])
            # if it's not on the same machine
            if minion["ip"] != "localhost":
                os.chdir('C:')
                # closing connection
                os.system("net use p: /delete")
        except:
            minion["state"] = "error"
