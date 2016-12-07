##############################################################
#
# File :- twilio_use.py
#
#Description :- This file implements the SMS logic
#
#Author :- Team Fantastic4
#
###############################################################

from twilio.rest import TwilioRestClient
message=""
# put your own credentials here
ACCOUNT_SID = 'AC42a81cddc97b00c9f7e086deae7201e7' #Will add the authorization on the demo day
AUTH_TOKEN = '55efaf36d23012f806dbf23b0e8539e6'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
def setRoute(route):
    print "inside teilio_use--> setRoute"
    global message
    message=route
    print message
def sendMessage(number):
    print "inside teilio_use--> send message"
    global body
    client.messages.create(
        to=number,
        from_='+14093163978 ',
        #body=body,
        body=message,
    )