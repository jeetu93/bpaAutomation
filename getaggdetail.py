'''# get access to lagg peering device information'''

import requests
import json

'''provide hostnames with comma seperated if multiple hosts'''

hostnames = input("Please provide hostnames : ")
url = "http://100.67.249.20:2680/bits_automation/web/api/device/get-aggregator"

hostdata = {
    "hostnames": "{}".format(hostnames)
    }


payload = json.dumps(hostdata)

headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic YWRtaW46MTIzNDU2",
    }

response = requests.request("POST", url, data=payload, headers=headers)

print("\n")
#print(response.text)

aggresult = json.dumps(json.loads(response.text), indent=4)
print("topology service fetched agg devices succesfully >")
print(aggresult)

