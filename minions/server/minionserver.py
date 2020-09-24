from flask import Flask, request
import requests
import os
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)


def server(host, port):
    app.run(host, port, debug=True)


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'
