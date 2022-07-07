# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 11:23:52 2022

@author: Marlou
"""

import ctypes, sys
import subprocess
import os
import re 

def get_consol_encoding():  # Возвращает тип кодировки консоли
    str_response = os.popen('chcp').read().split(':')[1].replace(' ', '')
    print("Consol encode - ",str_response)
    return(str_response)

def get_indexs_of_line_in_list(list_str_text, str_line):
    list_indexs = []
    for i in range(len(list_str_text)):
        if re.search(str_line, list_str_text[i]):
            list_indexs.append(i)
        if len(list_indexs) == 1 : return list_indexs[0]
    return(list_indexs)

def del_firsts_spaces(str_line):
    for i in range(len(str_line)):
        if str_line[i] != ' ': 
            return(str_line[i:])

def get_actual_self_ip(dict_main_self_info):
    result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE).stdout.decode(encoding=get_consol_encoding(),errors='ignore').split('\n')
    result = result[get_indexs_of_line_in_list( result, dict_main_self_info['net_name'])+2 : get_indexs_of_line_in_list( result, dict_main_self_info['net_name'])+7]
    dict_main_self_info['self_ip'] = del_firsts_spaces(result[2].split(':')[1][:-1])
    dict_main_self_info['net_ip']  = del_firsts_spaces(result[4].split(':')[1][:-1])
    return(dict_main_self_info)
    

dict_main_self_info = {'net_name': 'Беспроводная сеть', 'GUID': '2aa13434-d872-40f0-92a6-423d08e47af9', 'MAC': 'b4:0e:de:8c:5f:af', 'SSID': 'RT-5GPON-3350', 'BSSID': '10:a3:b8:f1:33:52', 'Input': '866.7', 'Output': '866.7', 'Signal_lvl': '97%'}

print(get_actual_self_ip(dict_main_self_info))