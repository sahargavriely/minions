from flask import Flask, request
import requests
import os
import hashlib
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


def server(host, port):
    app.run(host, port, debug=True)


@app.route('/')
def hello_world():
    return "<h1>Hello, I'm a hardworking minion!</h1>"


@app.route('/crack', methods=['GET'])
def crack():
    data = request.json
    hashed_password = data["hashed password"]
    f, t = data["from"], data["to"]
    for i in range(f, t):
        addition = str(i)
        phone_number = "05" + "0"*(8-len(addition)) + addition
        if hashlib.md5(phone_number.encode()).hexdigest() == hashed_password:
            return {"password": phone_number}
    return {"password": "not found"}