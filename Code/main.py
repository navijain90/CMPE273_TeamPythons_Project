from __future__ import absolute_import

import json
import BusinessLogic
import re

import ast
from flask import jsonify
import os
from urlparse import urlparse


#Persistent DB
# Creating Data Base if not created already
from model import db
from model import createdb
from model import TripResult
createdb()
# creating table if not already created
db.create_all()

from flask import Flask, render_template, request, Response, redirect, session
#from flask_sslify import SSLify
#from rauth import OAuth2Service
#from ast import literal_eval
import requests
import requests
import Lyft
import uber
import twilio_use
pattern = re.compile('[^A-Za-z0-9 -]')

app = Flask(__name__)

@app.route('/',methods=['GET'])
def welcome():
	return render_template('refer.html')

@app.route('/price', methods=['GET'])
def priceGet():
    return render_template('refer.html')

@app.route('/analysis', methods=['GET'])
def analyse():
    from sqlalchemy import func
    uberPriceList=[]
    lyftPricelist=[]
    lyftcount = ""
    ubercount = ""
    try:
        analysis_query = db.session.query(TripResult.bestprovider, func.count(TripResult.id).label('count'),func.sum(TripResult.uberprice).label('totaluber'),func.sum(TripResult.lyftprice).label('totallyft')).group_by(TripResult.bestprovider).all()
        for row in analysis_query:

            if row.bestprovider == "LYFT":
                lyftcount=row.count
            if row.bestprovider == "UBER":
                ubercount = row.count

        analysis_query_last_rows = db.session.query(TripResult.uberprice,TripResult.lyftprice).order_by(TripResult.id.desc()).limit(10).all()
        for row in analysis_query_last_rows:
            uberPriceList.append(round(float(str(row.uberprice)),2))
            lyftPricelist.append(round(float(str(row.lyftprice)),2))
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print e
        return render_template('server_error.html', result=e)

    analysis_result = {'ubercount': ubercount, 'lyftcount': lyftcount, 'uberPriceList': uberPriceList, 'lyftPricelist': lyftPricelist}
    return render_template('analysis.html', result=analysis_result)



@app.route('/price', methods=['POST'])
def price():
    dest = request.form['latlong']
    source = request.form['sourcelatlong']

    locationList = [source]

    DestList = dest.split(';')

    source_dest_list = request.form['sourceDestinationList']

    locationList.extend(DestList)
    BusinessLogic.setParameters(len(locationList))
    try:
        lyftOptimalPathList, lyftPriceList, useRoutepriceLyft = Lyft.lyftPrice(locationList)
        uberOptimalPathList, uberPriceList, cordinateList, priceList, serviceNameList,userRouteUberPrice = uber.uberPrice(locationList)
    except Exception as e:

        print e
        if str(e) == "1":
            return render_template('404.html', result=e)
        else:
            return render_template('server_error.html')
    print '\n'
    print uberPriceList
    print lyftPriceList
    print priceList
    print source_dest_list

    #optimalRoute = {"BestRouteUsingLyft": lyftOptimalPathList, "BestRouteUsingUber": uberOptimalPathList, "BestRouteUsingBoth": cordinateList, "BestPrice": priceList, "InvolvedProviders": serviceNameList }

    optimalRoute = {'BestRouteUsingLyft': lyftOptimalPathList, 'PriceForLyft': lyftPriceList,
                    'PriceForUber': uberPriceList, 'BestRouteUsingUber': uberOptimalPathList,
                    'BestRouteUsingBoth': cordinateList, 'BestPrice': priceList, 'InvolvedProviders': serviceNameList, 'userInput': source_dest_list, 'useRoutepriceLyft':  useRoutepriceLyft, 'userRouteUberPrice': userRouteUberPrice}

    totaluberprice = sum(uberPriceList)
    totallyftprice = sum(lyftPriceList)
    optimalPrice=sum(priceList)
    bestprovider = "LYFT"
    if(totallyftprice > totaluberprice):
        bestprovider = "UBER"
    totalpriceList = sum(priceList)
    locationDesc = source_dest_list.split(';')
    sourcelocation = locationDesc[0]
    destinations = locationDesc[1:]
    x= ', '.join(destinations)


    print totallyftprice
    print type(totallyftprice)
    try:
        db_obj = TripResult(sourcelocation=sourcelocation, destinations=x, uberprice=totaluberprice,
                            lyftprice=totallyftprice, optimalprice=totalpriceList,
                            bestprovider=bestprovider)
        db.session.add(db_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print e
        return render_template('server_error.html', result=e)


    mes_dict={}
    print "*************************************************************************************"
    print priceList
    print serviceNameList
    print cordinateList
    print source_dest_list
    print "*************************************************************************************"
    userInput=source_dest_list.split(";")
    for i in range(0,len(userInput)):
        part1= int(userInput[i].split(":")[0])-1
        part1=str(part1)
        part= userInput[i].split(":")[1].split(",")[0]
        print part
        part2=pattern.sub('',part)
        dictin={part1:part2}
        mes_dict.update(dictin)
    print mes_dict
    j=0
    str_mes=""
    for i in range(0,len(cordinateList)):
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++="
        j=i
        j=j+1
        if(j>=len(cordinateList)):
            j=0
        print cordinateList[i]
        print j,type(j)
        print cordinateList[j]
        print mes_dict[cordinateList[i]]
        print mes_dict[cordinateList[j]]
        print mes_dict[cordinateList[i]]+" --> "+mes_dict[cordinateList[j]]
        print serviceNameList[i]

        str_mes=str_mes+(mes_dict[cordinateList[i]]+" --> "+mes_dict[cordinateList[j]]+" via("+serviceNameList[i]+") \n")

    route= str_mes+"Total price = $"+str(totalpriceList)
    print route
    twilio_use.setRoute(route)
    return render_template('display.html', result=optimalRoute)

@app.route('/notify', methods=['POST'])
def sendRoute():
    number=request.form['PhoneNumber']
    print number
    #message=request_json['Route']
    twilio_use.sendMessage(number)
    print "Message sent"
    return render_template('refer.html')




if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1',port=8080)
