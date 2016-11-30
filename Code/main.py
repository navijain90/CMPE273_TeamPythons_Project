from __future__ import absolute_import

import json
import BusinessLogic
import ast
from flask import jsonify
import os
from urlparse import urlparse

from flask import Flask, render_template, request, Response, redirect, session
#from flask_sslify import SSLify
#from rauth import OAuth2Service
#from ast import literal_eval
import requests
import requests
import Lyft
import uber

app = Flask(__name__)




@app.route('/',methods=['GET'])
def welcome():
	return render_template('refer.html')

@app.route('/price', methods=['POST'])
def price():

    dest = request.form['latlong']
    source = request.form['sourcelatlong']
    locationList = [source]

    DestList = dest.split(';')

    locationList.extend(DestList)
    BusinessLogic.setParameters(len(locationList))

    lyftOptimalPathList, lyftPriceList = Lyft.lyftPrice(locationList)
    uberOptimalPathList, uberPriceList, cordinateList, priceList, serviceNameList = uber.uberPrice(locationList)
    print '\n'
    print lyftOptimalPathList
    print lyftPriceList
    print uberOptimalPathList
    print uberPriceList
    print cordinateList
    print priceList
    print serviceNameList

    #optimalRoute = {"BestRouteUsingLyft": lyftOptimalPathList, "BestRouteUsingUber": uberOptimalPathList, "BestRouteUsingBoth": cordinateList, "BestPrice": priceList, "InvolvedProviders": serviceNameList }

    optimalRoute = {'BestRouteUsingLyft': lyftOptimalPathList, 'PriceForLyft': lyftPriceList,
                    'PriceForUber': uberPriceList, 'BestRouteUsingUber': uberOptimalPathList,
                    'BestRouteUsingBoth': cordinateList, 'BestPrice': priceList, 'InvolvedProviders': serviceNameList}


    return render_template('display.html', result=optimalRoute)



if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1',port=8080)
