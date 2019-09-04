
# Author: ROHIT KADAM

#Book1.csv was a file imported from site which contains data regarding all the sites in an organizaion and their respective devices while in this code we extracted only the sites and checked if devices
# as given in the list "m" for these specific sites are present in NB or not. 

import requests
import json
import subprocess as sp
fp = open('C:\\Users\\rokadam\\Desktop\\Book1.csv')

x = fp.read()
y = x.split('\n')
# print (y)

for item in y:
    if len(item) == 0:
        y.pop(y.index(item))

z = []
for item in y:
    z.append(item.split(','))      #In case sometimes in the output you see /t instead of ',' replace ',' with '/t' in this line
# print (z)

a = []
for j in z:
    a.append(j[1])

a.remove('Site')
#print(a)


m = ['fpi-main','spi-main','rpi-wan']
n=[]
for item in a:
    for jtem in m:
        n.append('{}-{}'.format(item, jtem))
#print (n)                     #list of all devices that need to be checked in NB
print ("\n")
p=','.join(n)                #editing list to be passed to be passed as strings to get method
print ("Complete list of devices to be checked in netbrain database\n",len(p))

####################################### Checking status of these devices in netbrain through api   ##################################################

#print (p)
headers = {'NetOps-API-Key': ''}
r = requests.get("http://sjc04p1autap01:9090/netops/api/v1/netbrain/status?host={}".format(p), headers=headers)

q = r.json()
#print (q)

k=[]
#count=0
for item in q["output"]:
    if item["status_code"] == 404:
        k.append(item["object"])
    else:
        pass
        #r.append(q.index(item))
print ("List of devices not present in Netbrain:\n",k)

print ("No. of devices not present in NB:\n",len(k))

############################################ ckeck if devices are reachable ########################################################

l=[]
not_reachable=[]
for device in k:
    status,result = sp.getstatusoutput("ping -n 3 -w 5 " + str(device))
    #print (result)

    if "unreachable" in result:
        #print("System " + str(device) + " is UNREACHABLE !")
        pass
    elif status == 0:
        #print("System " + str(device) + " is UP !")
        l.append(device)
    else:
        print ("System " + str(device) + " is DOWN !")
        not_reachable.append(device)        # saving to further reolve the name and check for reachability using IP address! :)
print ("List of devices to be added to NB:\n",l)       #devices that are reachable and not present in netbrain!
print ("No. of devices which are reachable:\n",len(l))


########################################### Add reachable devices to Netbrain through API #############################################

t=','.join(l)
payload=[{"hostlist":"{}".format(t)}]
s = requests.post("http://your-server", json=payload, headers=headers)
u = s.json()
print (u)



