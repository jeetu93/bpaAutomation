import requests
import json
from inventory import *
from bpatoken import gettoken,host


def getorderinfo():

    token = gettoken()
    auth = "Bearer {}".format(token)
    url = "https://{}/bpa/api/v1.0/pointservice/orderDetails".format(host)
    
    service_tag_names = ["CEN-L2", "CEN-L3", "MPLS", "ISP"]
    all_order_data = []

    # Define start and end dates (keeping them hardcoded for now as per plan)
    start_date_str = "14-05-2020 00:00:00"
    end_date_str = "18-05-2020 23:59:59"

    headers = {
        'Authorization': auth,
        'Accept': "*/*",
        'Host': host,
        'Connection': "keep-alive",
    }

    for service_tag in service_tag_names:
        print(f"Fetching order details for {service_tag} from {start_date_str} to {end_date_str}...")
        body = {
            "startDate": start_date_str,
            "endDate": end_date_str,
            "serviceTagName": service_tag
        }

        try:
            response = requests.request("POST", url, data=json.dumps(body), headers=headers, verify=False) # Send body as JSON
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

            response_data = response.json()

            if 'data' in response_data and isinstance(response_data['data'], list):
                all_order_data.extend(response_data['data'])
                print(f"Successfully fetched {len(response_data['data'])} orders for {service_tag}.")
            elif 'data' not in response_data:
                print(f"Warning: 'data' key not found in response for {service_tag}. Response: {response_data}")
            else:
                print(f"Warning: 'data' in response for {service_tag} is not a list. Response: {response_data}")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching {service_tag}: {http_err}")
            print(f"Response content: {response.text}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred while fetching {service_tag}: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error occurred while fetching {service_tag}: {json_err}. Response text: {response.text}")

    if all_order_data:
        # Structure the final JSON to be similar to the original single service output,
        # with all orders under a top-level 'data' key.
        final_output_json = {"data": all_order_data}
        logresult = json.dumps(final_output_json, indent=4)

        with open("data.json", 'w') as log_file:
            log_file.write(logresult)
        print("Combined order logs created successfully in data.json >")
    else:
        print("No data fetched for any service tag. data.json will not be updated/created.")
        # Create an empty data.json if no data was fetched to prevent createCsvReport.py from failing if it expects the file
        final_output_json = {"data": []}
        logresult = json.dumps(final_output_json, indent=4)
        with open("data.json", 'w') as log_file:
            log_file.write(logresult)
        print("Created an empty data.json.")


    return logresult

#print("Date format is DD-MM")
#start_date = input("Please give start date : ")
#end_date = input("Please give end date : ")
#getorderinfo()
