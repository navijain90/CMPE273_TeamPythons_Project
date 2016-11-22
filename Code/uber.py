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


#============================


import random
import argparse
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


userDestination=raw_input("Please enter number of destination you are going\n")

parser = argparse.ArgumentParser()
parser.add_argument('--Destiantion', default = userDestination, type = int,
                     help='No of Destination User wants to travel.')
parser.add_argument('--tsp_use_random_matrix', default=True, type=bool,
                     help='Use random cost matrix.')
parser.add_argument('--tsp_random_forbidden_connections', default = 0,
                    type = int, help='Number of random forbidden connections.')
parser.add_argument('--tsp_random_seed', default = 0, type = int,
                    help = 'Random seed.')
parser.add_argument('--light_propagation', default = False,
                    type = bool, help = 'Use light propagation')

#========================



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
    list1=['1','2','3','4']
    #list2 = ['1', '2', '3', '4']

    pricelistmatrix=[]
    for i in range(4):
        pricelistmatrix.append([])
        for j in range(4):
            pricelistmatrix[i].append(0)

    pricelist=[]

    list=[]
    d = {}
    print "inside"
    url = config.get('base_uber_url_v1_2') + '/estimates/price'
    print url
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
                    pricelistmatrix[int(i)-1][counter]=int(d.get(k))
                    counter=counter+1

                    print d.get(k),

        print pricelistmatrix
        # pricelistmatrix.append(pricelist)
        # pricelist=[]



    print pricelistmatrix


    for i in range(len(pricelistmatrix)):
        for j in range(i,len(pricelistmatrix)):
            print pricelistmatrix[i][j]
            pricelistmatrix[j][i]=pricelistmatrix[i][j]

    obj= try_tsp.RandomMatrix(4, 0, pricelistmatrix)
    try_tsp.tsp(parser.parse_args(),pricelistmatrix)

    if response.status_code != 200:
        return 'There was an error', response.status_code

    return response.text

if __name__ == '__main__':
    app.run('127.0.0.1',port=8080)