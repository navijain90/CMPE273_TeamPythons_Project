from twilio.rest import TwilioRestClient
message=""
# put your own credentials here
ACCOUNT_SID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #Will add the authorization on the demo day
AUTH_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

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
        from_='+19518214747',
        #body=body,
        body=message,
    )