
"""
@author: Marlou
"""

"""
https://russianblogs.com/article/5838278912/ <- Запуск кода от имени администратора
https://askdev.ru/q/zapusk-komandy-obolochki-iz-python-i-zahvat-vyvoda-1412/ <- Ввод-вывод командной строки
"""

"""
netsh wlan set hostednetwork mode=allow ssid="ИМЯ_СЕТИ" key="ПОРОЛЬ_8_СИМВОЛОВ" <- Создание беспроводной сети
netsh wlan set hostednetwork mode=allow ssid="test_Network" key="12345678"
netsh wlan start hostednetwork <- Запуск беспроводной сети
netsh wlan set hostednetwork mode=disallow <- Для точного запуска сети 1-ая команда
netsh wlan set hostednetwork mode=allow <- Для точного запуска сети 2-ая команда

netsh wlan stop hostednetwork <– останавливает раздачу Wi-Fi
netsh wlan show settings <– выводит информацию о сети и отображает ее состояние.
NETSH WLAN show hostednetwork
netsh wlan connect name=ИмяПрофиляСети <- Для подключения к WiFi сети служит команда

netsh interface show interface
CLS <- очистка консоли windows
"""
"""
netstat -na|find "10000"
netsh wlan show driver
netsh wlan show interface
arp -a
ipconfig /displaydns
ipconfig /all
ipconfig
getmac
netsh interface show interface
netsh wlan show networks <- Отображает доступные подключения по wifi

chcp <- узнать текущую кодировку консоли
"""

# from __future__ import print_function
import ctypes, sys
import subprocess
import os
import re 

def is_admin(): # Проверка запущена ли консоль от имени администратора
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def do_command(list_commands): # Выполняет список команд в консоли от имени админестратора
    if is_admin(): # Добавьте код для запуска здесь
        for i in range(len(list_commands)):
            subprocess.run(list_commands[i], shell=True)
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            pass
            # ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

def get_splited_list(list_to_split,str_deltimetr = ':'): # Возвращает значения списка элементов, отделённых дельтиметром
    list_result = []
    for line in list_to_split:
        # list_result.append(line.replace(' ','').split(str_deltimetr, 1)[1][:-1])
        list_result.append(line.split(str_deltimetr, 1)[1][:-1])
    return list_result

def get_consol_encoding():  # Возвращает тип кодировки консоли
    str_response = os.popen('chcp').read().split(':')[1].replace(' ', '')
    print("Consol encode - ",str_response)
    return(str_response)

def get_net_driver_info():  # Возвращает тип сетевого драйвера
    str_netDriver = os.popen('netsh wlan show driver').readlines()[3].split(':')[1][1:]
    print("Net driver - ", str_netDriver)
    return(str_netDriver)

def del_firsts_spaces(str_line): # Удаляет все пробелы в начале текста
    for i in range(len(str_line)):
        if str_line[i] != ' ': 
            return(str_line[i:])

def get_indexs_of_line_in_list(list_str_text, str_line): # Возвращает список индексов вхождений строки в списке строк
    list_indexs = []
    for i in range(len(list_str_text)):
        if re.search(str_line, list_str_text[i]):
            list_indexs.append(i)
        if len(list_indexs) == 1 : return list_indexs[0]
    return(list_indexs)
    
def get_actual_self_ip(dict_main_self_info): # Добавляет в словарь основных данных информацию о собственном  ip и ip машины, раздающей сеть
    result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE).stdout.decode(encoding=get_consol_encoding(),errors='ignore').split('\n')
    result = result[get_indexs_of_line_in_list( result, dict_main_self_info['net_name'])+2 : get_indexs_of_line_in_list( result, dict_main_self_info['net_name'])+7]
    dict_main_self_info['self_ip'] = del_firsts_spaces(result[2].split(':')[1][:-1])
    dict_main_self_info['net_ip']  = del_firsts_spaces(result[4].split(':')[1][:-1])
    return(dict_main_self_info)

def get_self_info_in_dict(): # Взвращает словарь даннах о текущем соединениие 
    result = subprocess.run(['netsh', 'wlan', 'show', 'interface'], stdout=subprocess.PIPE).stdout.decode(encoding=get_consol_encoding(),errors='ignore').split('\n')
    result = get_splited_list(result[3:19])
    dict_main_self_info = {'net_name':del_firsts_spaces(result[0]),'GUID':result[2].replace(' ',''),'MAC':result[3].replace(' ',''),'SSID':result[5].replace(' ',''),'BSSID':result[6].replace(' ',''),'Input':result[13].replace(' ',''),'Output':result[14].replace(' ',''),'Signal_lvl':result[15][:-1].replace(' ','')}
    dict_main_self_info = get_actual_self_ip(dict_main_self_info)
    return(dict_main_self_info)


def main() -> None:
    dict_main_self_info = get_self_info_in_dict()
    print(dict_main_self_info)
main()
