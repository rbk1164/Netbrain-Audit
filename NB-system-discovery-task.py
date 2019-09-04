# Author: ROHIT KADAM

import requests
import json

#################################### Get the token ####################################################################

def get_token():
    url = "https://netbrain-API"

    headers = {"Content-Type": "application/json"}

    payload = {"username":"username", "password":"password", "authentication_id": "AD"}

    get_token  = requests.post(url, json=payload, headers=headers)

    token = (get_token.json()['token'])

    return token

################################## New Discovery####################################################################

def new_discovery(token):
    url = "https://netbrain-API-server"

    headers = {"Token":token, "Content-Type": "application/json"}

    new_discovery = requests.get(url, headers=headers)

    list_of_devices = (new_discovery.json())
    ouput_file = input("Please enter the file where you want to save the data:")
    new_file = open(ouput_file,"w")
    csv_headers = 'mgmtIP,source,hostname,ping,\n'
    new_file.write(csv_headers)
    count=0
    for item in (list_of_devices['devices']):
        if 'hostname' not in item:
            count+=1
            x = ('{},{},{},{},\n'.format(item['mgmtIP'],item['source'],'',item['ping']))
            new_file.write(x)

        elif 'ping' not in item:
            count+=1
            new_file.write('{},{},{},{},\n'.format(item['mgmtIP'],item['source'],item['hostname'],''))

        elif 'mgmtIP' not in item:
            count+=1
            new_file.write('{},{},{},{},\n'.format('',item['source'],item['hostname'],item['ping']))

        elif 'source' not in item:
            count+=1
            new_file.write('{},{},{},{},\n'.format(item['mgmtIP'],'',item['hostname'],item['ping']))

        else:
            count+=1
            new_file.write('{},{},{},{},\n'.format(item['mgmtIP'],item['source'],item['hostname'],item['ping']))

    new_file.close()
    print (count)


##################################### Go into right tenant/domain ##################################################

def get_tenant_domain():
    url = "https://netbrain-API"
    token = get_token()
    headers = {"Token":token, "Content-Type": "application/json"}

    payload = {"tenantId":"", "domainId":""}

    get_tenant_domain = requests.put(url, data=json.dumps(payload), headers=headers)

    new_discovery(token)

get_tenant_domain()
