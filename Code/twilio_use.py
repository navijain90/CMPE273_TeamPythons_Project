from twilio.rest import TwilioRestClient
body=""
# put your own credentials here
ACCOUNT_SID = 'ACa9eaa9afdf09bbfe1da3b67282727d1b'
AUTH_TOKEN = '647b45cab2a4dddd6a9caad0de1cffa6'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
def setRoute(route):
    global body
    body=route
def sendMessage(number):
    global body
    client.messages.create(
        to=number,
        from_='+19518214747',
        #body=body,
        body="Test",
    )