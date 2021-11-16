import json
import csv
#from GetLogsNpayloads import *
#from GetPayloadByDate import *

with open('data.json', 'r') as f:

    file = json.loads(f.read())
    #print(type(file))
    d = file['data']
    #print(d)

    data_list = []

    total_ra = []
    ra_failed = []
    ra_success = []
    ra_inprogress = []
    
    # below three status are for cen-l2 only
    cen_l2_success = []
    cen_l2_failed = []
    cen_l2_inprogress = []


    for items in d:
        # print(type(items))
	#.encode("utf-8")
        logsNpayload = {}
        #payload = items["formData"].encode("utf-8")
	payload = items["formData"]
        service_list = ['mpls-l2vpn-cfs:mpls-l2vpn', 'cen-link', 'link',
			 'internet-link', 'eci-l2vp.encode("utf-8"n-cfs:eci-l2vpn-cfs',
                         'eci-l2vpn-cfs:eci-l2vpn-cfs']
        # 1 Get_order_number
        for key in dict(payload):
            try:
                if key in service_list:
                    orderNumber = payload[key][0]['order']['ra']
               
                if key == "mpls-l2vpn-cfs:mpls-l2vpn":
                    cen_status = items['status']
		    #print(cen_status)
                    if cen_status == "Success":
		        cenPass = payload[key][0]['order']['ra']
            	        cen_l2_success.append(cenPass)
                    elif cen_status == "Failed":
                        cenFail = payload[key][0]['order']['ra']
                        cen_l2_failed.append(cenFail)
		    else:
			cenInp = payload[key][0]['order']['ra']
                        cen_l2_inprogress.append(cenInp)

            except KeyError:
                orderNumber = '0'

            # 2 Get_status_msg
        try:
            statusmsg = items['statusMessage']
        except KeyError:
            statusmsg = "no key found"

        # 3 Get_Dry_run
        try:
            dryrun = items['dryRunResponse']
        except KeyError:
            dryrun = "no dry run found"

        # 4 Get status and staus report
        status = items["status"]

        if status == "Success":
            ra_success.append(orderNumber)
        elif status == "Failed":
            ra_failed.append(orderNumber)
        else:
            ra_inprogress.append(orderNumber)

        total_ra.append(orderNumber)

        # 5 now create the dictionary of choice of data
        logsNpayload['status'] = items["status"]
        logsNpayload['status_msg'] = statusmsg
        logsNpayload['ra'] = orderNumber
        logsNpayload['dryrun'] = dryrun
        logsNpayload['payload'] = payload
        logsNpayload['update_time'] = items["updatedAt"]
        logsNpayload['ckt_id'] = items["CircuitID"]
        logsNpayload['service_type'] = items["serviceTagName"]

        data_list.append(logsNpayload)

# with open('report.csv','a') as newfile:
with open('report.csv', 'w') as newfile:
    fieldnames = ['ra', 'status', 'status_msg', 'ckt_id',
	 'service_type', 'dryrun', 'payload', 'update_time']
    csv_writer = csv.DictWriter(newfile, fieldnames=fieldnames)
    csv_writer.writeheader()

    for rows in data_list:
        csv_writer.writerow(rows)

    print("CSV file write done! ")

# finding failed unique RA numbers those are clear failed and never gat passed that day
failed_unique = []
failed_1st_then_pass = []
for i in ra_failed:
    if i in ra_success:
        #print("ra failed first but passed later", i)
        failed_1st_then_pass.append(i)
    elif i not in ra_success:
        #print("failed unique", i)
        failed_unique.append(i)

failed = []
for x in failed_unique:
    if x not in failed:
        failed.append(x)
# for x in failed:
#    print(x)

# print(failed)
Total = failed + ra_success + ra_inprogress
print("###############################################")
print('\nReport consolidated')
# print("\nTotal Failed Orders list : ",ra_failed)
# print("\nFailed Then Passed list : ",failed_1st_then_pass)
print("\nTotal RA numbers are : ", Total)
print("\nPassed Orders list : ", ra_success)
print("\nExact Failed Orders list : ", failed)
print("\nInProgress Orders list : ", ra_inprogress)
print("failed_1st_then_pass  : ", failed_1st_then_pass)
print('\n')

print("###############################################")
print("COUNT: Total Numbers of Orders", " : ", len(Total))
print("COUNT: Exact Passed RA count", " : ", len(ra_success))
print("COUNT: Exact Failed Orders", " : ", len(failed))
print("COUNT: In Progress RA count", " : ", len(ra_inprogress))
print("\n")
print("Total Number of orders are : ",len(Total))
print("\n")
print("---------End of overall report----------")
print("\n")


# finding failed unique RA numbers those are clear failed and never gat passed that day



# remove duplicacy from the list

def Unique(list1,list2):
    U_list1 = []
    U_list2 = []
    for i in list1:
        if i in list2:
            #print("ra failed first but passed later", i)
            U_list2.append(i)
        elif i not in list2:
            #print("failed unique", i)
            U_list1.append(i)
    unik_list = []
    for x in U_list1:
        if x not in unik_list:
            unik_list.append(x)
    return unik_list
    #print(unik_list)

list1 = cen_l2_failed
list2 =  cen_l2_success
unik_list = Unique(list1,list2)
cen_failed = unik_list

print("				CEN-L2 UAT Report				")
print("\n")
print("CEN-L2 SUCCESS ORDERS : ",len(cen_l2_success))
print("\n")
print(cen_l2_success)
print("\n")
print("CEN-L2 FAILED ORDERS : ")
print("\n")
print(cen_failed)
print("\n")
print("CEN-L2-INPROGRESS ORDERS : ",len(cen_l2_inprogress))
print("\n")
print(cen_l2_inprogress)

#print(cen_l2_failed)
#for items in cen_l2_failed:
#    print(type(items))
