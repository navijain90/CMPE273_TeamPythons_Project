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



@app.route('/',methods=['GET'])
def welcome():
	return render_template('refer.html')


uberpricelistmatrix=[]
locationList = []
@app.route('/location', methods=['POST'])
def my_form_post():

    dest = request.form['latlong']
    source = request.form['sourcelatlong']
    sourceDestinationList = request.form['sourceDestinationList']

    locationList = [source]
    DestList = dest.split(';')
    locationList.extend(DestList)

    #print locationList
    dictionary = dict(u.split(":") for u in sourceDestinationList.split(";"))
    #print dictionary



    list1=['1','2','3','4']
    d = {}

    for i in range(len(locationList)):
        uberpricelistmatrix.append([])
        for j in range(len(locationList)):
            uberpricelistmatrix[i].append(0)

    url = 'https://api.uber.com/v1.2/estimates/price'

    for i in range(len(locationList)):
        print '\n'
        counter = int(i)
        for j in range(int(i)+1,len(locationList)+1,1) :
            param={
                'start_latitude': locationList[i-1].split(',')[0],
                'start_longitude': locationList[i-1].split(',')[1],
                'end_latitude': locationList[j-1].split(',')[0],
                'end_longitude': locationList[j-1].split(',')[1],
            }

            print locationList[i-1].split(',')[0]
            print locationList[i-1].split(',')[1]
            print locationList[j-1].split(',')[0]
            print locationList[j-1].split(',')[1]
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

    for i in range(len(uberpricelistmatrix)):
        for j in range(i, len(uberpricelistmatrix)):
            uberpricelistmatrix[j][i] = uberpricelistmatrix[i][j]

    BusinessLogic.Optimalprice(uberpricelistmatrix)
    BusinessLogic.CombinedOptimal(uberpricelistmatrix,'UBER')


    if response.status_code != 200:
        return 'There was an error', response.status_code

    return response.text









#uberpricelistmatrix=[]

#@app.route('/uber/price', methods=['GET'])
'''
def uberPrice():


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

    for i in range(len(uberpricelistmatrix)):
        for j in range(i, len(uberpricelistmatrix)):
            uberpricelistmatrix[j][i] = uberpricelistmatrix[i][j]

    BusinessLogic.Optimalprice(uberpricelistmatrix)
    BusinessLogic.CombinedOptimal(uberpricelistmatrix,'UBER')


    if response.status_code != 200:
        return 'There was an error', response.status_code

    return response.text
'''

if __name__ == '__main__':
     app.run('127.0.0.1',port=8080)