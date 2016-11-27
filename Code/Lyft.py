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
def lyftPrice(locationList):
    list1 = ['1', '2', '3', '4']

    #lyftpricelistmatrix = []
    #Initiliaze the list to 0
    for i in range(len(locationList)):
        lyftpricelistmatrix.append([])
        for j in range(len(locationList)):
            lyftpricelistmatrix[i].append(0)
    print lyftpricelistmatrix

    d = {}
    #print "inside"
    url = 'https://api.lyft.com/v1/cost'
    for i in range(len(locationList)):
        print '\n'
        counter = int(i)
        for j in range(int(i) + 1, len(locationList) + 1, 1):
            print "inside j Lyft loop"
            param = {
                'start_lat': locationList[i-1].split(',')[0],
                'start_lng': locationList[i-1].split(',')[1],
                'end_lat': locationList[j-1].split(',')[0],
                'end_lng': locationList[j-1].split(',')[1],
            }
            response = app.requests_session.get(
                url,
                headers=generate_ride_headers('gAAAAABYNRqZS_x7fOJQpH5-qDrtq6-Zyzy8ONTDuWJAFELjruND-Ipbh-aIs9fJ0rgSx9Ljf4rnxXVn6DQscHO1dWj0wfccucXwoqw9uRJpaSrNunPPaEQL3Hh1TFa1sdJ3MOi9_kqKs4XrZU7Ur8ikOFjWrLIZ3R9lyBwbsb2A3c57YnfZg6U='),
                params=param,
            )
            print "inside j Lyft loop: After request"
            if response.status_code != 200:
                return 'There was an error', response.status_code
            print response.json()
            for key, value in response.json().iteritems():
                for x in value:
                    if x['ride_type'] == 'lyft':
                        d = x
            for k, v in d.iteritems():
                if (k == "estimated_cost_cents_min"):
                    print d.get(k)
                    lyftpricelistmatrix[int(i) - 1][counter] = int(d.get(k))/100
                    counter = counter + 1

                    print d.get(k),


    for i in range(len(lyftpricelistmatrix)):
        for j in range(i,len(lyftpricelistmatrix)):
            lyftpricelistmatrix[j][i]=lyftpricelistmatrix[i][j]

    lyftOptimalPathList = BusinessLogic.Optimalprice(lyftpricelistmatrix)
    BusinessLogic.CombinedOptimal(lyftpricelistmatrix,'LYFT')
    #print "LYFT : " + x + list1 + listNames
    return lyftOptimalPathList

#
# if __name__ == '__main__':
#     print "Inside Run"
#     app.run('127.0.0.1',port=8000)