from __future__ import absolute_import

import json
import ast
from flask import jsonify
import os
from urlparse import urlparse

from flask import Flask, render_template, request, redirect, session
from flask_sslify import SSLify
from rauth import OAuth2Service
from ast import literal_eval
import requests

#app = Flask(__name__, static_folder='static', static_url_path='')
app = Flask(__name__)
app.requests_session = requests.Session()

with open('config.json') as f:
    print "file opened"
    config=json.load(f)

base_url=config.get('base_uber_url_v1_2')
print base_url

def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'Token %s' % token,
        'Content-Type': 'application/json',
    }

@app.route('/',methods=['POST'])
def welcome():
	return "Welcome to the Web Service App"

@app.route('/price', methods=['GET'])
def price():
    print "inside"
    url = config.get('base_uber_url_v1_2') + '/estimates/price'
    print url
    params = {
        'start_latitude': config.get('start_latitude'),
        'start_longitude': config.get('start_longitude'),
        'end_latitude': config.get('end_latitude'),
        'end_longitude': config.get('end_longitude'),
    }

    response = app.requests_session.get(
        url,
        headers=generate_ride_headers('Xx4BN5agMH44QKdUwE10Jp1XwQAztdxwA_0-jRaJ'),
        params=params,
    )
    # return response.json.get('prices')
    # return jsonify({response.text})
    # print response.json
    # return response.json
    # resp=response.text.split(":")[1]
    # print resp
    #
    # return ast.literal_eval(response.text)
    print response.status_code

    if response.status_code != 200:
         return 'There was an error', response.status_code
    #data=json.loads(response.text)
    # print data['prices']
    # my_dict = literal_eval(response.text)
    #print type(response.text)
    #data=json.load(response.text)

    return response.json()




    # data=str(response.text)
    # o = json.loads(data)
    # print o
    # return o
    # for resp in obj["prices"]:
    #     print resp
    #
    # return jsonify(response.text)
    # '''return render_template(
    #     'results.html',
    #     endpoint='price',
    #     data=response.text,
    # )'''
if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1',port=8080)