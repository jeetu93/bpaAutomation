# get bpa token for authentication
from inventory import *
import json
import requests

host = PROD2['host']
auth = PROD2['Authorization']

def gettoken():

    url = "https://{}/bpa/login".format(host)
    authentication = "Basic {}".format(auth)

    headers = {
    'Authorization': authentication,
    'Accept': "*/*",
    'Host': host,
    'Connection': "keep-alive",
    }

    response = requests.request("POST", url, headers=headers, verify=False)
    #print(response.text)
    token = json.loads(response.text)['access_token']
    #print(token)
    return token

#gettoken()
