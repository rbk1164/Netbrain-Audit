# Author: ROHIT KADAM


import multiprocessing.dummy
import multiprocessing
import time
import subprocess as sp
import time
import multiprocessing
import subprocess as sp

imported_file = input('imported file: ')
#output_file  = input('Where do you want the output:')
with open(imported_file,'r',encoding='utf-16') as f:
#print(f.readlines()[11])
    gateway_ip = []
    for row in f.readlines():

        if '8' in row.split('\t')[2] and int(row.split('\t')[7])<=27:
            ip = row.split('\t')[3].split('.')
            ip[3] = str(int(ip[3]) + 1)
            gateway_ip.append('.'.join(ip))
        else:
            pass
#print (gateway_ip)
starttime = time.time()
def snmp_query(ip):
    #with open(output_file,'w') as f:
    #f.write('Gateway_IP, Type of Device,\n')
    status,result = sp.getstatusoutput('snmpget -v 2c -c <community-string> {} SNMPv2-MIB::sysDescr.0'.format(ip))
   # print (gateway_ip,'---',result)
    if 'Juniper' in result:
        #f.write('{},Juniper,\n'.format(ip))
        print("{} Juniper".format(ip))
    elif 'Palo Alto' in result:
        #f.write('{},Palo Alto,\n'.format(ip))
        print("{} Palo Alto".format(ip))
    else:
        print (result)
        print ("Nothing happening")
    return True

def snmp_multiprocessing():
    num_threads = 6 * multiprocessing.cpu_count()
    p = multiprocessing.dummy.Pool(num_threads)
    p.map(snmp_query, gateway_ip)

if __name__ == "__main__":
    snmp_multiprocessing()

print('That took {} seconds'.format(time.time() - starttime))
