# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 16:56:22 2022

@author: Marlou
"""

import subprocess


def get_splited_list(list_to_split,str_deltimetr = ':'):
    list_result = []
    for line in list_to_split:
        list_result.append(line.replace(' ','').split(str_deltimetr, 1)[1][:-1])
    return list_result


result = subprocess.run(['netsh', 'wlan', 'show', 'interface'], stdout=subprocess.PIPE).stdout.decode(encoding='CP866',errors='ignore').split('\n')
a = result
result = get_splited_list(result[3:19])
print(result)
dict_main_info = {'GUID':result[2],'MAC':result[3],'SSID':result[5],'BSSID':result[6],'Input':result[13],'Output':result[14],'Signal_lvl':result[15][:-1]}
print(dict_main_info)
# print(type(result))