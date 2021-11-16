import requests
import json
from inventory import *
from bpatoken import gettoken,host


def getorderinfo():

    token = gettoken()
    auth = "Bearer {}".format(token)

    url = "https://{}/bpa/api/v1.0/pointservice/orderDetails".format(host)
    
    body = {
        "startDate":"14-05-2020 00:00:00",
        "endDate":"18-05-2020 23:59:59",
	"serviceTagName": "CEN-L2"
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
    #print(logresult)
    with open("data.json",'w') as log:
        log.write(logresult)
        print("logs Created succesfully >")

    return logresult

#print("Date format is DD-MM")
#start_date = input("Please give start date : ")
#end_date = input("Please give end date : ")
#getorderinfo()
