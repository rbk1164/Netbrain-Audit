# Author: ROHIT KADAM


#Netbrain7 and Netbrain6 weekly audit

################## checking the devices present in NB6 and not in NB7 and vice versa #############################
# Entries in NB7 are of paramount importance
#run this code for weekly NB audit
import os
import requests
import json
import subprocess as sp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import getpass
from easygui import passwordbox

output_file = input("Please enter the file where you want the devices present in 6 and not in 7 to be saved in as: ")
def ping_function(device):
    status,result = sp.getstatusoutput("ping -n 2 -w 2 " + str(device))
    if "unreachable" in result:
        return "unreachable"
    elif status == 0:
        return "reachable"
    else:
        return "request timed out/hostname not found"



def audit_Netbrain(netbrain6_file, netbrain7_file):

    netbrain6_new_list = []
    netbrain7_new_list = []

    netbrain6 = open(netbrain6_file).read().split("\n")
    netbrain7 = open(netbrain7_file).read().split("\n")

    for line in netbrain6:
        if not line:
            pass
        else:
            hostname = line.split(",")[2].strip()
            if "-rpi-" in hostname or "-spi-" in hostname or "-fpi-" in hostname:
                netbrain6_new_list.append(hostname)
            else:
                pass
    #print (netbrain6_new_list)

    for line in netbrain7:
        hostname = line.split(",")[0].strip('"')
        if "-rpi-" in hostname or "-spi-" in hostname or "-fpi-" in hostname:
            netbrain7_new_list.append(hostname)
        else:
            pass
    #print (netbrain7_new_list)


    devices_in_6_not_in_7 = []
    devices_in_6_not_in_7.append(list(set(netbrain6_new_list) - set(netbrain7_new_list)))


    for device in devices_in_6_not_in_7:
        devices_in_6_not_in_7_new_list = device

    with open(output_file,'w') as f:
        f.write('Device in 6 not in 7,Ping,\n')
        for device in devices_in_6_not_in_7_new_list:
            ping_output = ping_function(device)
            f.write('{},{},\n'.format(device,ping_output))
        f.close()
    '''headers = {'NetOps-API-Key': ''}
    payload=[{"hostlist":"{}".format(devices_in_6_not_in_7)}]
    add_devices_to_NB7 = requests.post("http://server", json=payload, headers=headers)
    print('\n',add_devices_to_NB7.json(),'\n')

    #headers = {'NetOps-API-Key': ''}
    get_pushed_devices = requests.get("http://your-server?host={}".format(devices_in_6_not_in_7), headers=headers)
    get_pushed_devices = get_pushed_devices.json()
    devices_in_7_after_push = []
    devices_not_in_7_after_push = []
    for item in get_pushed_devices['output']:
        if item['status_code'] == 200:
            devices_in_7_after_push.append(item['object'])
        else:
            devices_not_in_7_after_push.append(item['object'])

    print ('Devices present in NB7 after push: ',devices_in_7_after_push)
    print('\nDevices not present in NB7 after push: ',devices_not_in_7_after_push)
'''
    #************************************* devices present in NB6 but not in NB7 need to be pushed to NB7, create a module for pushing this and also use mail module to mail these files

def send_file_through_mail():

    email_user = ''
    email_password = passwordbox("email password: ")
    email_send = ''

    subject = 'List of Devices not in 7 but present in 6'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    msg['Bcc'] = email_user

    body = 'Hi! \nI have attached the file devices present in 6 but not in 7 and their reachability. \n\nThank you, \n\nSincerely,\nRohit Kadam'
    msg.attach(MIMEText(body,'plain'))

    filename=output_file
    attachment = open(filename,'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('your-smtp-server',25)
    server.starttls()
    server.login(email_user,email_password)


    server.sendmail(email_user,email_send,text)
    server.quit()


netbrain6_file = input("Please enter the Netbrain6 file :")
netbrain7_file = input("Please enter the Netbrain7 file :")

audit_Netbrain(netbrain6_file, netbrain7_file)
send_file_through_mail()
