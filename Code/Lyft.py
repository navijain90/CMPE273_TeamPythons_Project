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
import try_tsp
lyftpricelistmatrix = []


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




def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'bearer %s' % token,
        'Content-Type': 'application/json',
    }

@app.route('/lyft',methods=['GET'])
def welcome():
	return render_template('refer.html')

@app.route('/lyft/price', methods=['GET'])
def price():
    list1 = ['1', '2', '3', '4']

    #lyftpricelistmatrix = []
    #Initiliaze the list to 0
    for i in range(4):
        lyftpricelistmatrix.append([])
        for j in range(4):
            lyftpricelistmatrix[i].append(0)
    print lyftpricelistmatrix

    #pricelist = []

    #list = []
    d = {}
    #print "inside"
    url = config.get('base_lyft_url') + '/v1/cost'
    print url
    for i in list1:
        print '\n'
        counter = int(i)
        for j in range(int(i) + 1, len(list1) + 1, 1):
            print "inside j loop"
            param = {
                'start_lat': config.get('latitude' + i),
                'start_lng': config.get('longitude' + i),
                'end_lat': config.get('latitude' + str(j)),
                'end_lng': config.get('longitude' + str(j)),
            }
            response = app.requests_session.get(
                url,
                headers=generate_ride_headers('gAAAAABYNRqZS_x7fOJQpH5-qDrtq6-Zyzy8ONTDuWJAFELjruND-Ipbh-aIs9fJ0rgSx9Ljf4rnxXVn6DQscHO1dWj0wfccucXwoqw9uRJpaSrNunPPaEQL3Hh1TFa1sdJ3MOi9_kqKs4XrZU7Ur8ikOFjWrLIZ3R9lyBwbsb2A3c57YnfZg6U='),
                params=param,
            )
            print "inside j loop: After request"
            if response.status_code != 200:
                return 'There was an error', response.status_code

            for k, v in response.json().iteritems():
                d = v[2]
            for k, v in d.iteritems():
                if (k == "estimated_cost_cents_min"):
                    lyftpricelistmatrix[int(i) - 1][counter] = int(d.get(k))/100
                    counter = counter + 1

                    print d.get(k),

        print lyftpricelistmatrix
        # pricelistmatrix.append(pricelist)
        # pricelist=[]

    print lyftpricelistmatrix

    for i in range(len(lyftpricelistmatrix)):
        for j in range(i, len(lyftpricelistmatrix)):
            print lyftpricelistmatrix[i][j]
            lyftpricelistmatrix[j][i] = lyftpricelistmatrix[i][j]

    obj = try_tsp.RandomMatrix(4, 0, lyftpricelistmatrix)
    try_tsp.tsp(parser.parse_args(), lyftpricelistmatrix)



    return response.text


if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1',port=5005)