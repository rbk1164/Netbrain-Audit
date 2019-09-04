# Author: ROHIT KADAM


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
    z.append(item.split('\t'))     #In case sometimes in the output you see /t instead of ',' replace ',' with '/t' in this line
print (z)


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
print ("Complete list of devices to be checked in NB:\n",p)

print ("\n")
#print ("Complete list of devices to be checked in netbrain database\n",len(p))

####################################### Checking status of these devices in netbrain through api   ##################################################

headers = {'NetOps-API-Key': ''}
r = requests.get("http://your-netbrain-server?host={}".format(p), headers=headers)

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
print ("\n")
#print ("No. of devices not present in NB:\n",len(k))

############################################ ckeck if devices are reachable ########################################################

l=[]
not_reachable=[]
cannot_ping=[]
for device in k:
    status,result = sp.getstatusoutput("ping -n 3 -w 5 " + str(device))
    #print (result)

    if "unreachable" in result:
        #print("System " + str(device) + " is UNREACHABLE !")
        not_reachable.append(device)
        pass
    elif status == 0:
        #print("System " + str(device) + " is UP !")
        l.append(device)
    else:
        #print ("System " + str(device) + " is DOWN !")
        cannot_ping.append(device)                                                   # saving to further reolve the name and check for reachability using IP address! :)
print ("List of devices which can be reached and need to be added to NB:\n",l)       #devices that are reachable and not present in netbrain!
print ("\n")
#print ("No. of devices which are reachable:\n",len(l))

print ("Destination Unreachable Devices:\n",not_reachable)
print ("\n")
print ("Other devices that cannot be reached due to some other reason:\n",cannot_ping)
print ("\n")


########################################### Write the devices to be added to the new csv file ###########################################
def add_to_file():
    fp = open('C:\\Users\\rokadam\\Desktop\\Book1.csv','r')

    x = fp.read()
    y = x.split('\n')
    #print (y)


    z = []
    for item in y:
        z.append(item.split('\t'))
    #print (z[0])

    z[0].append("Missing reachable Devices added to NB")
    #print(z[0])


    count=0
    for items in range(len(z)):
        if items == 0:
            pass
        else:
            z[items].append(l[count])
            count+=1
            if count == (len(l)):
                break
            else:
                continue
    resultz= []
    for element in z:
        resultz.append(",".join(element))

    final = "\n".join(resultz)

    fp.close()                    ####### the file open in read need to be closed


    write_to_file = open('C:\\Users\\rokadam\\Desktop\\Book3.csv','w')      ###write operation performed on a completely new file!!!

    write_to_file.write(final)          #### the write operation can be performed only once, meaning if we execute the same code again,
                                              # the module conatining write operation will give an error stating that the permission is denied


########################################### Add reachable devices to Netbrain through API #############################################

t=','.join(l)
payload=[{"hostlist":"{}".format(t)}]
s = requests.post("http://your-netbrain-server", json=payload, headers=headers)
u = s.json()
print (u)

add_to_file()      ######## call to add to the new file the complete list missing and added devices

