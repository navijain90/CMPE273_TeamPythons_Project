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
import BusinessLogic
lyftpricelistmatrix = []



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
#
# @app.route('/lyft',methods=['GET'])
# def welcome():
# 	return "Welcome"
# 	#return render_template('refer.html')

#@app.route('/lyft/price', methods=['GET'])
def lyftPrice():
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


    for i in range(len(lyftpricelistmatrix)):
        for j in range(i,len(lyftpricelistmatrix)):
            lyftpricelistmatrix[j][i]=lyftpricelistmatrix[i][j]

    BusinessLogic.Optimalprice(lyftpricelistmatrix)
    BusinessLogic.CombinedOptimal(lyftpricelistmatrix,'LYFT')
    return response.text

#
# if __name__ == '__main__':
#     print "Inside Run"
#     app.run('127.0.0.1',port=8000)