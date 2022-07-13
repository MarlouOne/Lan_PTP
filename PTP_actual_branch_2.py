
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



##############################################################################
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

##############################################################################
from threading import Thread, Event
import socket
import sys


# global gl_dict_clients # Глобальный список подключенных соединений
# gl_dict_clients = {}

def get_self_ip():
    # global gl_dict_main_self_info 
    return client.gl_dict_main_self_info['self_ip']

class client():
    gl_dict_clients = {}
    str_ip : str
    int_port : int
    main_sock : socket.socket
    mirror_sock : socket.socket
    
    
    def __int__(self,str_ip, int_port, int_mode, new_socket = ""):
        
        if int_mode == 1: # Если мы звоним
            self.str_ip    = str_ip
            self.int_port  = int_port 
            self.main_sock = new_socket 
            thread_calling = Thread(target=self.th_call_to_client, args = (), daemon=False)
            thread_calling.start()
        
        
        
        elif int_mode == 2: # Если нам звонят
            pass
    
    def th_call_to_client(self):
        print('Start colling...')
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        bool_connection_stat = False
        int_try_counter = 0
        
        print(f'Calling to {self.str_ip} on {self.int_port}...')
        
        while bool_connection_stat == False or int_try_counter != 4: # В случае если мы не смогли подключится или подключились

            try:
                sock.connect( (self.str_ip, self.int_port) )

                self.sock = sock
                bool_connection_stat = True
                
                client.gl_dict_clients[self.str_ip] = self
                
                client.gl_dict_clients[self.str_ip].info()
                
                print(f'Connected to {self.str_ip} on {self.int_port}.')
                thread_reception = Thread(target=self.th_reception_messages, args=(), daemon=False)
                thread_reception.start()

                sys.exit()
                
            except Exception:
                continue
        
        print(f'Timeout to {self.str_ip} on {self.int_port}.')
        
        sock.close()
        sys.exit()

class listener():
    static_int_port_to_connect = 10000
    
    def __init__(self):
        if listener.bool_flag_to_listen == True:
            thread_listening = Thread(target=self.eternal_listen, args = (), daemon=False)
            thread_listening.start()
            
        
    def eternal_listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = (get_self_ip(), self.static_int_port_to_connect)
    
        sock.bind(server_address)
        sock.listen(1)  

        while True:
            try:
                print('Ready for get connection.')
                new_socket, list_client_info = sock.accept()
                print(f'Connected with {list_client_info[0]} by port {list_client_info[1]}')
                      
                client.gl_dict_clients[list_client_info[0]] = client(list_client_info[0], list_client_info[1], 2, new_socket)
                sock.close()
                
                thread_listening = Thread(target=self.eternal_listen, args = (), daemon=False)
                thread_listening.start()
                break
                
            except Exception:
                # print('error')
                continue
            
        sys.exit()




def make_open_chat():
    # global gl_dict_clients
    listener()

    str_input_command = ''
    print(client.gl_dict_clients)
    
    while str_input_command != '-с':
        for i in range(  len( list(client.gl_dict_clients) )  ):
            print(i+1, '. ', client.gl_dict_clients[ list(client.gl_dict_clients)[i] ].info, sep='')
        
        
        str_input_command = str(input('Введете указание : '))
        # соедини с -192.168.137.180  #соедини с -192.168.232.30 # соедини с -192.168.0.11
        if re.search('соедини с -', str_input_command):
            str_IP_to_connect = (str_input_command.split('-')[1])
            client(str_IP_to_connect, 10000)
        
        elif re.search('покажи список клиентов', str_input_command):
            client.show_clients_socket_info()
            
        # напиши -192.168.137.180 # напиши -192.168.0.11
        elif re.search('напиши -', str_input_command):
            str_IP_to_write = (str_input_command.split('-')[1])
            client.gl_dict_clients[str_IP_to_write].write_to()

    #     # закрой соединение с -192.168.137.180
    #     elif re.search('закрой соединение с -', str_input_command):
    #         str_IP_to_terminate = (str_input_command.split('-')[1])
    #         dict_connections[str_IP_to_terminate].kill_listener()

    # for i in range(len(list(dict_connections))):
    #     dict_connections[list(dict_connections)[i]].kill_listener()
    #     # print("Соединение с ", list(dict_connections)[i] , "закрыто." )

    sys.exit()

##############################################################################
def main() -> None:
    global gl_dict_main_self_info 
                                    # {'net_name': 'Беспроводная сеть', 'GUID': '2aa13434-d872-40f0-92a6-423d08e47af9', 'MAC': 'b4:0e:de:8c:5f:af', 'SSID': 'RT-5GPON-3350',
                                    #  'BSSID': '10:a3:b8:f1:33:52', 'Input': '702', 'Output': '866.7', 'Signal_lvl': '95%', 'self_ip': '192.168.0.6',
                                    #  'net_ip': '192.168.0.1'}
    gl_dict_main_self_info = get_self_info_in_dict()
    print(gl_dict_main_self_info)
    make_open_chat()
main()
