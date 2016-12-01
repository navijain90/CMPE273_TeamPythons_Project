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
#import try_tsp
#from itertools import tee, islice, chain, izip
import BusinessLogic


app = Flask(__name__)
app.requests_session = requests.Session()


def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'Token %s' % token,
        'Content-Type': 'application/json',
    }

# @app.route('/uber',methods=['POST'])
# def welcome():
#     return "Welcome to the Web Service App"


uberpricelistmatrix=[]


def uberPrice(locationList):
    d = {}

    for i in range(len(locationList)):
        uberpricelistmatrix.append([])
        for j in range(len(locationList)):
            uberpricelistmatrix[i].append(0)

    url = 'https://api.uber.com/v1.2/estimates/price'

    for i in range(len(locationList)-1):
        print '\n'
        counter = int(i)
        for j in range(int(i)+1,len(locationList),1) :
            param={
                'start_latitude': locationList[i].split(',')[0],
                'start_longitude': locationList[i].split(',')[1],
                'end_latitude': locationList[j].split(',')[0],
                'end_longitude': locationList[j].split(',')[1],
            }

            print locationList[i].split(',')[0]
            print locationList[i].split(',')[1]
            print locationList[j].split(',')[0]
            print locationList[j].split(',')[1]
            response = app.requests_session.get(
                url,
                headers=generate_ride_headers('Xx4BN5agMH44QKdUwE10Jp1XwQAztdxwA_0-jRaJ'),
                params=param,
            )

            for k, v in response.json().iteritems():
                d = v[1]
            for k, v in d.iteritems():
                if (k == "low_estimate"):
                    uberpricelistmatrix[int(i)][counter+1]=float(d.get(k))
                    counter=counter+1

                    print d.get(k),

    for i in range(len(uberpricelistmatrix)):
        for j in range(i, len(uberpricelistmatrix)):
            uberpricelistmatrix[j][i] = uberpricelistmatrix[i][j]

    uberOptimalPathList, uberPriceList = BusinessLogic.Optimalprice(uberpricelistmatrix)
    cordinateList, priceList, serviceNameList = BusinessLogic.CombinedOptimal(uberpricelistmatrix,'UBER')


    if response.status_code != 200:
        return 'There was an error', response.status_code
    #print "UBER : " + x + list1 + listNames

    # added by Bhavika to calculate price for route as added by user
    userRouteUberPrice = []
    for s in range(len(uberpricelistmatrix) - 1):
        value = uberpricelistmatrix[s][s + 1]
        userRouteUberPrice.append(value)
        if (s == (len(uberpricelistmatrix) - 2)):
            val = uberpricelistmatrix[s + 1][0]
            userRouteUberPrice.append(val)


    return uberOptimalPathList, uberPriceList, cordinateList, priceList, serviceNameList,userRouteUberPrice

# if __name__ == '__main__':
#     app.run('127.0.0.1',port=8080)
