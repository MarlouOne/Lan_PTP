# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 19:30:19 2022

@author: Marlou
"""

import os
import threading
import socket
from datetime import datetime

global dict_Other_users

dict_Other_users = {'IP':[],'Status':[],'Name':[],'MAC':[]}

def getMyIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def scan_Ip(ip, str_Self_Ip):
    global dict_Other_users
    
    addr = str_Self_Ip + str(ip)
    comm = "ping -n 1 -a " + addr
    response = os.popen(comm)
    data = response.readlines()

    for line in data:
        if ( '['+ addr +']' ) in line:
            dict_Other_users['IP'].append(addr)
            dict_Other_users['Status'].append('Ping_Ok')
            
            break

def find_other_users():
    global dict_Other_users
    
    str_Self_Ip = getMyIp()
    print('You IP :',str_Self_Ip)
    net_split = str_Self_Ip.split('.')
    str_Self_Ip = net_split[0] + '.' + net_split[1] + '.' + net_split[2] + '.'
    
    start_point = 1
    end_point = 255
    print(f'Search from {start_point} to {end_point}')
    
    int_Tine_Start = datetime.now()
    print("Scanning in Progress:")
    print('IP                 Status          Name            MAC')
    for ip in range(start_point, end_point):
        # scan_Ip(ip,str_Self_Ip)
        if ip == int(net_split[3]):
            continue
        thread_Target = threading.Thread(target=scan_Ip, args=[ip,str_Self_Ip])
        thread_Target.start()
        
    thread_Target.join()
    int_Tine_End = datetime.now()
    int_Total_Time = int_Tine_End - int_Tine_Start

    print ('Find ip :',len(dict_Other_users['IP']))
    print("Scanning completed in: ", int_Total_Time)
    
    # dict_Other_users = json.dumps(strin,separators='|')
    
find_other_users()

print(dict_Other_users)