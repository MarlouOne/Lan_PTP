# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 17:39:34 2022

@author: Marlou
"""

import os
import threading
import socket
from datetime import datetime

import json
import re


##############################################################################

global gl_list_Other_users
gl_list_Other_users = []


def scan_Ip(ip, str_Self_Ip):
    global gl_list_Other_users
    
    str_user_IP = str_Self_Ip + str(ip)
    comm = "ping -n 1 -a " + str_user_IP
    response = os.popen(comm)
    data = response.readlines()
    dict_user_info = {}
    for line in data:
        if ( '['+ str_user_IP +']' ) in line:
            dict_user_info = {"Type": "User", "Login": None, "IP": str_user_IP, "MAC": get_user_MAC(str_user_IP), "Port": 10000}
            gl_list_Other_users.append(dict_user_info)
            # {"Type": "Self", "Login": "rrr", "IP": "192.168.8.100", "MAC": "B4-0E-DE-8C-5F-AF", "Status": "UFC"}         
            break

def find_other_users(str_File_root):
    global gl_list_Other_users
    
    str_Self_Ip = get_self_IP()
    # print('You IP :',str_Self_Ip)
    net_split = str_Self_Ip.split('.')
    str_Self_Ip = net_split[0] + '.' + net_split[1] + '.' + net_split[2] + '.'
    
    start_point = 1
    end_point = 255
    print(f'Search from {start_point} to {end_point}')
    
    int_Tine_Start = datetime.now()
    # print("Scanning in Progress:")
    # print('IP                 Status          Name            MAC')
    for ip in range(start_point, end_point):
        # scan_Ip(ip,str_Self_Ip)
        if ip == int(net_split[3]):
            continue
        thread_Target = threading.Thread(target=scan_Ip, args=[ip,str_Self_Ip])
        thread_Target.start()
        
    thread_Target.join()
    int_Tine_End = datetime.now()
    int_Total_Time = int_Tine_End - int_Tine_Start
    
    upd_json_File(gl_list_Other_users, str_File_root)
    
    print(gl_list_Other_users)
    print ('Find ip :',len(gl_list_Other_users))
    print("Scanning completed in: ", int_Total_Time)
    
##############################################################################

def merging_lists(list_One, list_Two):
    # list_New = list_One
    for item in list_Two:
        if type(item) == list:
            for lists_item in item:
                list_One.append(lists_item)
        else:
            list_One.append(item)
    return list_One

def upd_json_File(new_Data, str_File_root):
    save_data = []
    if os.path.getsize(gl_str_Data_root) != 0:
        with open(str_File_root, 'r') as file: 
            # Сохраняем старое содержимое файла
            save_data = json.load(file)
            
    if type(save_data) == list:
        save_data = merging_lists(save_data, new_Data)
    else :
        save_data = [save_data, new_Data]
        
    with open(str_File_root, 'w') as file:
        # Записываем в файл новые
        file.write(json.dumps(save_data))


def get_user_MAC(str_user_IP):
    response = os.popen("arp -a")
    lines = response.readlines()
    for line in lines:
        if re.search(str_user_IP, line) and ":" not in line:
            # re.search('hello', 'hello world')
            MAC = " ".join(line.split()).replace(" ", "$").split("$")[1]
            return MAC

def get_self_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

class user:
    str_self_Name : str
    str_self_IP : str
    str_self_MAC : str

    def show_self_info(self):
        print('Self info : ',self.str_self_Name, self.str_self_IP, self.str_self_MAC)
    
    def get_self_MAC(self):
        response = os.popen("getmac")
        line = response.readlines()[3]
        MAC = " ".join(line.split()).replace(" ", "$").split("$")[0]
        return MAC
    
    def __init__(self, str_File_root):
        # global gl_str_Data_root

        # print('='*10)
        if input("Заходите первый раз ? (Y/N) - ").capitalize() == 'Y' : 
            # Логин в первый раз 
           self.str_self_Name = (input("Введите имя пользователя в сети - "))
           self.str_self_IP = get_self_IP()
           self.str_self_MAC = self.get_self_MAC()
           
           upd_json_File({'Type':'Self', 'Login':self.str_self_Name,'IP':self.str_self_IP,'MAC':self.str_self_MAC,'Status': 0}, str_File_root)
           # print('='*10)
        else : 
            save_data = []
            if os.path.getsize(str_File_root) != 0:
                with open(str_File_root, 'r') as file: 
                    # Сохраняем старое содержимое файла
                        save_data = json.load(file)
                        
            if type(save_data) == dict : save_data = [save_data]
            
            list_Positions = []
            for i in range(len(save_data)):
                a = save_data[i]['Type']
                if save_data[i]['Type'] == 'Self' :
                    list_Positions.append(i)
                    print(len(list_Positions),save_data[i])
            
            int_trigger = int(input('Выберите нужную запись - ')) - 1
            self.str_self_Name = save_data[list_Positions[int_trigger]]['Login']
            self.str_self_IP = get_self_IP()
            self.str_self_MAC = self.get_self_MAC()
           
            print('='*10)      
        
        self.show_self_info()

##############################################################################

def make_open_chat(str_File_root):
    global gl_list_Other_users
    list_clients = []
    str_input_command = ''
    

    
    while str_input_command != '-стоп':
        for i in range(len(gl_list_Other_users)): 
            print(i+1, gl_list_Other_users[i])
        
        str_input_command = str(input('Введете указание - '))
        if re.search('-соедини с', str_input_command):
            pass
        
        elif re.search('-ищи', str_input_command):
            gl_list_Other_users = []
            find_other_users(gl_str_Data_root)


def main():
    global gl_str_Data_root 
    gl_str_Data_root = r"C:\Users\major\Desktop\PTP_LAN_Chat\Test_Vareables\Data.txt"
    
    print("Programm start")
    user_obj = user(gl_str_Data_root)
    find_other_users(gl_str_Data_root)
    # make_open_chat(gl_str_Data_root)
    print("Programm end")

main()


# def make_open_chat(str_File_root):
#     global gl_list_Other_users
#     list_clients = []
#     str_input_command = ''
    
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         # Привязываем сокет к порту
#         server_address = (get_self_IP(), 10000)
#         print('Старт сервера на {} порт {}'.format(*server_address))
#         server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         server_socket.bind(server_address)
#     except OSError:
#         server_socket.close()
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind(server_address)
        
#     # Слушаем входящие подключения
#     server_socket.listen(4)
    
#     while str_input_command != '-стоп':
#         for i in range(len(gl_list_Other_users)): 
#             print(i+1, gl_list_Other_users[i])
        
#         str_input_command = str(input('Введете указание - '))
#         if re.search('-соедини с', str_input_command):
#             pass
        
#         elif re.search('-ищи', str_input_command):
#             gl_list_Other_users = []
#             find_other_users(gl_str_Data_root)

        
        

# def make_new_connects(dict_user_info):
#     # {"Type": "Self", "Login": "rrr", "IP": "192.168.8.100", "MAC": "B4-0E-DE-8C-5F-AF", "Port": "10000"}  
#     # {"Type": "User", "Login": None, "IP": str_user_IP, "MAC": get_user_MAC(str_user_IP), "Port": 10000}
#     str_server_IP = dict_user_info['IP']
#     int_server_port = dict_user_info['Port']
#     sock_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock_connect.connect(str_server_IP,int_server_port)