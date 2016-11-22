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

#app = Flask(__name__, static_folder='static', static_url_path='')
app = Flask(__name__)
app.requests_session = requests.Session()






def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'bearer %s' % token,
        'Content-Type': 'application/json',
    }

@app.route('/',methods=['GET'])
def welcome():
   return render_template('ex.html')

@app.route('/price', methods=['GET'])
def price():
    url = 'https://api.lyft.com' + '/v1/cost'

    print url
    params = {
        'start_lat': '37.7772',
        'start_lng': '-122.4233',
        'end_lat': '37.7972',
        'end_lng': '-122.4533',
    }

    response = app.requests_session.get(
        url,
        headers=generate_ride_headers('gAAAAABYM1VWb_cNxyrE_4yX9hf7krHRaP1Vz0PNGuDMD7u9dk_WENqPMoSy-gFC4eI8SdE1WBMfzdE3irkdJ0pjUrxd5UPMmBwnUOhkQ39YSo-1gU71t9fNxo2_YPcXogrq-WkVBILXs8f-kbrl4AI1XxBnQzaYNDpRBQHeO1IablER05vj_MVFfclWz0EOx_g62HTy6DukIdaMM-UzLkL9PElK7b5NdQ=='),
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
    print type(response.text)
    data1 = response.text
    
    
    
    
    
    data = response.content
    print type(data)
    
   
    
    return data
   
    
    
if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1',port=5005)
