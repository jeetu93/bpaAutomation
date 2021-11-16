'''# sync bpa to nso cfs after any new device onboarded into NSO'''

import requests
import json
from bpatoken import gettoken,host

token = gettoken()
auth = "Bearer {}".format(token)

url = "https://100.67.249.2:30101/bpa/api/v1.0/settings/devices/sync?nsoInstance=NSO_CFS"

inputs = {
    "_id": "5db148648b54390026993b1e",
    "controllerType": "NSO",
    "host": "100.67.249.3",
    "name": "NSO_CFS",
    "scheme": "http",
    "port": "8080",
    "username": "bpauser",
    "password": "********",
    "zone": "Default",
    "lsa": "true",
    "default": "true",
    "__v": 0,
    "defaultname": "NSO_CFS (LSA) (Default)"
}

payload = json.dumps(inputs)

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': auth
}

response = requests.request("POST", url, headers=headers, data = payload, verify = False)
bpasyncresult = json.dumps(json.loads(response.text), indent=4)
#print(response.text.encode('utf8'))

print("Here is your bpa to nso sync result ")
print(bpasyncresult)
