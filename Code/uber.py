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
import try_tsp
from itertools import tee, islice, chain, izip
import BusinessLogic


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


uberpricelistmatrix=[]

@app.route('/price', methods=['GET'])
def price():


    list1=['1','2','3','4']
    d = {}

    for i in range(4):
        uberpricelistmatrix.append([])
        for j in range(4):
            uberpricelistmatrix[i].append(0)

    url = config.get('base_uber_url_v1_2') + '/estimates/price'

    for i in list1:
        print '\n'
        counter = int(i)
        for j in range(int(i)+1,len(list1)+1,1) :
            param={
                'start_latitude': config.get('latitude' + i),
                'start_longitude': config.get('longitude' + i),
                'end_latitude': config.get('latitude' + str(j)),
                'end_longitude': config.get('longitude' + str(j)),
            }
            response = app.requests_session.get(
                url,
                headers=generate_ride_headers('Xx4BN5agMH44QKdUwE10Jp1XwQAztdxwA_0-jRaJ'),
                params=param,
            )

            for k, v in response.json().iteritems():
                d = v[1]
            for k, v in d.iteritems():
                if (k == "low_estimate"):
                    uberpricelistmatrix[int(i)-1][counter]=int(d.get(k))
                    counter=counter+1

                    print d.get(k),

    BusinessLogic.price(uberpricelistmatrix)


    if response.status_code != 200:
        return 'There was an error', response.status_code

    return response.text

if __name__ == '__main__':
    app.run('127.0.0.1',port=8080)