from flask import Flask, request
import requests
import os
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)

minions = {}
minion_server = "print('hello word')"


def server(host, port):
    app.run(host, port, debug=True)


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/minions', methods=['POST'])
def set_up_minions():
    minions = request.json
    for minion in minions:
        minion["state"] = "up"
        if "port" not in minion:
            minion["port"] = "8000"
        try:
            os.system("net use p: \\\\" + minion["ip"] + "\\Users\\" + minion["username"] +
                      " " + minion["password"] + " /user:" + minion["username"])
            os.chdir('P:')
            os.system("mkdir Desktop\\minion")
            os.system("echo " + minion_server + "> Desktop\\minion\\minion.py")
            os.system("python Desktop\\minion\\minion.py")
            os.chdir('C:')
            os.system("net use p: /delete")
        except:
            minion["state"] = "error"
    return "minions"


@app.route('/crack', methods=['POST'])
def cracking():
    print(request.json)
    return "crack"
