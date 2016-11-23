from __future__ import absolute_import

import json
import ast
from flask import jsonify
import os
from urlparse import urlparse

from flask import Flask, render_template, request, redirect, session
#from flask_sslify import SSLify
#from rauth import OAuth2Service
#from ast import literal_eval
import requests
import requests
import Lyft
import uber

app = Flask(__name__)



@app.route('/',methods=['POST'])
def welcome():
    return "Welcome to the Web Service App"

@app.route('/price', methods=['GET'])
def price():
    Lyft.lyftPrice()
    uber.uberPrice()


if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1',port=8080)