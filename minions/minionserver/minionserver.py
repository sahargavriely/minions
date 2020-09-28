from flask import Flask, request
import requests
import os
import hashlib
import time


app = Flask(__name__)


def server(host, port):
    app.run(host, port, debug=True)


@app.route('/')
def hello_world():
    return "<h1>Hello, I'm a hardworking minion!</h1>"


@app.route('/crack', methods=['GET'])
def crack():
    data = request.json
    hashed_password = data["hashed password"]
    f, t = data["start from"], data["to"]
    minion_name = data["minion name"]
    os.system(r"mkdir cache\\cache%s" % (minion_name.replace(" ", "")))
    time.sleep(3)
    for i in range(f, t):
        addition = str(i)
        if i % 100000 == 0:
            os.system(r"echo %s > cache\cache%s\startfrom.txt" % (addition, minion_name.replace(" ", "")))
        phone_number = "05" + "0"*(8-len(addition)) + addition
        if hashlib.md5(phone_number.encode()).hexdigest() == hashed_password:
            return {"password": phone_number}
    return {"password": "not found"}


@app.route('/newfrom', methods=['GET'])
def new_start():
    data = request.json
    minion_name = data["minion name"]
    try:
        phone = read_file(minion_name)
    except:
        time.sleep(3)
        phone = read_file(minion_name)        
    print(phone)
    return {"start from": phone}


def read_file(minion_name):
    file = open(r"cache\cache%s\startfrom.txt" % (minion_name.replace(" ", "")), "r")
    phone = file.read()
    file.close()
    return phone