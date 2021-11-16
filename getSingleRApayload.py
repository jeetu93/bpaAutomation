import requests
import json
from inventory import *
from bpatoken import gettoken,host


def getorderinfo():

    token = gettoken()
    auth = "Bearer {}".format(token)

    url = "https://{}/bpa/api/v1.0/pointservice/orderDetails".format(host)
    
    body = {
        "ra":"{}".format(order),
    }

    headers = {
        'Authorization': auth,
        'Accept': "*/*",
        'Host': host,
        'Connection': "keep-alive",
    }

    response = requests.request("POST", url,data = body, headers=headers, verify=False)
    logresult = json.dumps(json.loads(response.text), indent=4)
    print("RA order logs fetched succesfully >")
    print(logresult)
    with open("singleRApayloaddata.json",'w') as log:
        log.write(logresult)
        print("logs Created succesfully >")

    return logresult

order = input("Please give order number : ")
getorderinfo()
