# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 13:30:09 2022

@author: Marlou
"""
import socket
import json
import os
import re


global str_gl_Data_root 
str_gl_Data_root = r"C:\Users\major\Desktop\PTP_LAN_Chat\Test_Vareables\Data.json"

def upd_json_File(new_Data, str_File_root):
    save_data = []
    if os.path.getsize(str_gl_Data_root) != 0:
        with open(str_File_root, 'r') as file: 
            # Сохраняем старое содержимое файла
            save_data = json.load(file)
            
    if type(save_data) == list:
        save_data += [new_Data]
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
        
class user:
    str_self_Name : str
    str_self_IP : str
    str_self_MAC : str

    def show_self_info(self):
        print(self.str_self_Name, self.str_self_IP, self.str_self_MAC)
    
    def get_self_MAC(self):
        response = os.popen("getmac")
        line = response.readlines()[3]
        MAC = " ".join(line.split()).replace(" ", "$").split("$")[0]
        return MAC
    
    def get_self_IP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
        s.connect(('<broadcast>', 0))
        return s.getsockname()[0]
    
    def __init__(self):
        global str_gl_Data_root
        print('='*10)
        # str_Flag = 
        print('='*10)
        if input("Заходите первый раз ? (Y/N) - ").capitalize() == 'Y' : 
            # Логин в первый раз 
           self.str_self_Name = (input("Введите имя пользователя в сети - "))
           self.str_self_IP = self.get_self_IP()
           self.str_self_MAC = self.get_self_MAC()
           
           upd_json_File({'Type':'Self', 'Login':self.str_self_Name,'IP':self.str_self_IP,'MAC':self.str_self_MAC,'Status':'UFC'}, str_gl_Data_root)
           print('='*10)
        else : 
            save_data = []
            if os.path.getsize(str_gl_Data_root) != 0:
                with open(str_gl_Data_root, 'r') as file: 
                    # Сохраняем старое содержимое файла
                        save_data = json.load(file)
                        
            if type(save_data) == dict : save_data = [save_data]
            
            list_Positions = []
            for i in range(len(save_data)):
                if save_data[i]['Type'] == 'Self' :
                    list_Positions.append(i)
                    print(len(list_Positions),save_data[i])
            
            int_trigger = int(input('Выберите нужную запись - ')) - 1
            self.str_self_Name = save_data[list_Positions[int_trigger]]['Login']
            self.str_self_IP = self.get_self_IP()
            self.str_self_MAC = self.get_self_MAC()
           
            print('='*10)      
        
        self.show_self_info()

def main():
    print("Programm start")
    user_obj = user()
    
    print("Programm end")

main()