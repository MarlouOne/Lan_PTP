# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 19:30:19 2022

@author: Marlou
"""

import os
import platform
import threading
import socket
from datetime import datetime
import json 

global strin, dict_Other_users

dict_Other_users = {'IP':[],'Status':[],'Name':[],'MAC':[]}
strin = []



def getMyIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def scan_Ip(ip, net):
    global dict_Other_users
    
    addr = net + str(ip)
    comm = ping_com + addr
    response = os.popen(comm)
    data = response.readlines()
    name = data[1].split(' ')
    for line in data:
        if 'TTL' in line:
            response_art = os.popen('arp -a')
            data_arp = response_art.readlines()
            for line_arp in data_arp:
                flag = line_arp.split()

                if len(flag) > 0 and flag[0] == addr:
                    tmp =(addr + '|' + "Ping_Ok"+ '|' + name[3]+ '|' +flag[1])
                    
                    dict_Other_users['IP'].append(addr)
                    dict_Other_users['Status'].append('Ping_Ok')
                    dict_Other_users['Name'].append(name[3])
                    dict_Other_users['MAC'].append(flag[1])
                    
                    strin.append(tmp)

            break

def find_other_users():
    global ping_com, dict_Other_users
    
    net = getMyIp()
    print('You IP :',net)
    net_split = net.split('.')
    net = net_split[0] + '.' + net_split[1] + '.' + net_split[2] + '.'
    # start_point = int(input("Enter the Starting Number: "))
    # end_point = int(input("Enter the Last Number: "))
    start_point = 1
    end_point = 255
    print(f'Search from {start_point} to {end_point}')

    
    oс = platform.system()
    if (oс == "Windows"):
        ping_com = "ping -n 1 -a "
    else:
        ping_com = "ping -c 1 "
    
    t1 = datetime.now()
    print("Scanning in Progress:")
    print('IP                 Status          Name            MAC')
    for ip in range(start_point, end_point):
        if ip == int(net_split[3]):
            continue
        potoc = threading.Thread(target=scan_Ip, args=[ip,net])
        potoc.start()
        #potoc.join()
    potoc.join()
    t2 = datetime.now()
    total = t2 - t1
    for i in strin:
        print(i)
    print ('Find ip :',len(strin))
    print("Scanning completed in: ", total)
    
    # dict_Other_users = json.dumps(strin,separators='|')
    
find_other_users()

print(dict_Other_users)