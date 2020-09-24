from flask import Flask, request
import requests
import os
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
def master_server():
    data = request.json
    minions = data["config"]
    set_up_minions(minions)
    cracking(minions, data["hashed_password"])
    return "again"


def set_up_minions(minions):
    for minion_name in minions:
        minion = minions[minion_name]
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


def cracking(minions, hashed_password):
    working_minions = 0
    for minion_name in minions:
        minion = minions[minion_name]
        if minion["state"] == "up":
            working_minions += 1
    i = 0
    for minion_name in minions:
        minion = minions[minion_name]
        minion["from"] = 99999999//working_minions * i
        i += 1
        minion["to"] = 99999999//working_minions * i
        try:
            minion["state"] = "searching"
            minion["search"] = requests.get(url="http://" + minion["host"] + ":" +
                                            minion["port"] + "/crack", json={"hashed password": hashed_password, "from": minion["from"], "to": minion["to"]}).json()["password"]
            print(minion["search"])
        except:
            minion["state"] = "error"
    return "cracked"
