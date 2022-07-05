# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 09:56:02 2022

@author: Marlou
"""

import threading
import socket

import re


def get_self_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def make_connection_and_listen(str_IP, int_port = 10000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (get_self_IP(), int_port)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    sock.listen(1)
    
    # th_reception_messages(sock, str_IP, int_port)
    
    thread_listen = threading.Thread(target=th_reception_messages, args = (sock, str_IP, int_port), daemon=True)
    thread_listen.start()
    
    # thread_listen = mp.Process(target=th_reception_messages, args = (sock, str_IP, int_port), daemon=False)
    # thread_listen.start()
    
    return thread_listen

    
    # sock.connect((str_IP, 10000))
    
def th_reception_messages(sock, str_IP, int_port):
    
    print(f'Ожидание соединения c {str_IP} по порту {int_port}...')
    try:
        connection, list_client_info = sock.accept() #ТУТ ПОЯВЛЯЕТСЯ ОШИБКА С АДРЕСССОМ - 
        # ГЛАВНЫЙ КОД ВЫРУБАЕТ СОКЕТ РАНЬШЕ, ЧЕМ КОНЧАЕТСЯ ЭТОТ ПОТОК Может быть)
    except WindowsError:
        print('error with sock')

    print(f'Налажено соединени c {str_IP} по порту {int_port}.')

    try:
        # Принимаем данные порциями и ретранслируем их
        while True:
            try:
                data = connection.recv(1024)
                if data.decode() == '-e':
                    print(f'Соединение с {str_IP} завершено.')
                    connection.close()
                    sock.close()
                    break
                    
                print(f'Получено от {str_IP}: {data.decode()}')
                if data:
                    connection.sendall('Доставлено'.encode())  
            except:
                continue
    except:
        # Очищаем соединение
        connection.close()
    sock.close()
    

def write_to():
    pass

global gl_list_Other_users
gl_list_Other_users = [{'Type': 'User', 'Login': None, 'IP': '192.168.137.180', 'MAC': '10-63-c8-9a-7e-cb', 'Port': 10000}]
# {'Type': 'User', 'Login': None, 'IP': '192.168.137.180', 'MAC': '10-63-c8-9a-7e-cb', 'Port': 10000}

def make_open_chat():
    global gl_list_Other_users
    global list_threads_switcher 
    list_threads_switcher 
    dict_connections = {}
    
    str_input_command = ''
    
    while str_input_command != '-стоп':
        for i in range(len(gl_list_Other_users)): 
            print(i+1, gl_list_Other_users[i])
        
        str_input_command = str(input('Введете указание : '))
        if re.search('соедини с -', str_input_command):
            str_IP_to_connect = (str_input_command.split('-')[1])
            
            # make_connection_and_listen(str_IP_to_connect, 10000)
            
            dict_connections[str_IP_to_connect] = make_connection_and_listen(str_IP_to_connect, 10000)
            
        elif re.search('напиши -', str_input_command):
            write_to()
        elif re.search('закрой соединение с -', str_input_command):
            str_IP_to_terminate = (str_input_command.split('-')[1])
            dict_connections[str_IP_to_terminate].terminate()
        
make_open_chat()