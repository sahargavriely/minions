from flask import Flask, request
import requests
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


def server(host, port):
    app.run(host, port, debug=True)


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/minions', methods=['POST'])
def set_up_minions():
    print(request.json)
    return "minions"


@app.route('/crack', methods=['POST'])
def cracking():
    print(request.json)
    return "crack"
