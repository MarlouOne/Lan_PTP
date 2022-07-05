# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 09:56:02 2022

@author: Marlou
"""

from threading import Thread, Event
import socket
import sys

import re


def get_self_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]
    
class listener():
    str_IP : str
    int_port : int
    bool_event = Event()
    bool_connection_stat = False
    sock : socket
    # connection : socket
    
    def print_listener_info(self):
        print(self.str_IP, self.int_port)
    
    def __init__(self, str_IP, int_port):
        self.int_port = int_port
        self.str_IP = str_IP
        self.bool_event.set()
        
        # self.th_reception_messages()
        
        thread_listen = Thread(target=self.th_reception_messages, args = (), daemon=False)
        thread_listen.start()

    def th_call_to_client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_address = ('192.168.137.1', self.int_port) #192.168.232.58 #192.168.137.1
        sock.bind(server_address)
        
        
        while self.bool_connection_stat == False :
            try :
                print('Calling...')
                sock.connect( (self.str_IP, self.int_port) )
                self.sock = sock  
                self.bool_connection_stat = True
                print('call stat is ok')
            except Exception:
                continue

        sys.exit()
            
        
    def th_wait_for_client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # print(get_self_IP())  #get_self_IP - Может некорректно отображаь IP в беспроводной сети. Требует переработки
        # server_address = (get_self_IP(), int_port) 
        
        server_address = ('192.168.137.1', self.int_port) #192.168.232.58 #192.168.137.1
        sock.bind(server_address)
        
        sock.listen(1)
        
        while self.bool_connection_stat == False :
            try :
                print('Waiting...')
                self.sock, list_client_info = sock.accept() 
                # self.sock = sock  
                self.bool_connection_stat = True
                print('wait stat is ok')
            except Exception:
                continue
            
  
        sys.exit()
        
        
    def th_reception_messages(self):
    
        # print("2",self.bool_event.is_set())
        print(f'Ожидание соединения от {self.str_IP} по порту {self.int_port}...')
        
        try:
             th_wait_for = Thread(target=self.th_wait_for_client, args = (), daemon=True)
             th_call_to  = Thread(target=self.th_call_to_client, args = (), daemon=True)
             th_wait_for.start()
             th_call_to.start()
             
        except WindowsError:
            print('error with sock')
            
        while self.bool_connection_stat == False :
            continue
        
            
        print(f'Налажено соединени c {self.str_IP} по порту {self.int_port}.')
    
        try:
            # Принимаем данные порциями и ретранслируем их
            while self.bool_event.is_set():
                # print("3",self.bool_event.is_set())
                try:
                    data = self.sock.recv(1024)
                    if data.decode() == '-e':
                        print(f'Соединение с {self.str_IP} завершено со стороны клиента.')
                        self.sock.close()
                        # self.sock.close()
                        break
                        
                    print(f'Получено от {self.str_IP}: {data.decode()}')
                    if data:
                        self.sock.sendall('Доставлено'.encode())  
                except:
                    continue
        except:
            # Очищаем соединение
            self.sock.close()
        print(f"Соединение с {self.str_IP} закрыто.")
        self.sock.close()
        sys.exit()
        
    def kill_listener(self):
        print(f"Соединение с {self.str_IP} отключено.")
        self.bool_event.clear()
        # print('4',self.bool_event.is_set())

    def write_to(self):

        try:
            # Отправка данных
            message = input(f'Отправить {self.str_IP} по порту {self.int_port}: ').encode()
            self.sock.sendall(message)
        
            # Смотрим ответ
            answer = self.sock.recv(1024)
            if answer:
                    print('Доставлено')
        except:
            pass
            # finally:
            #     print('Закрываем сокет')
            #     sock_for_connect.close()
                
        # sock.close()
        # sock_for_connect.close()

global gl_list_Other_users
gl_list_Other_users = [{'Type': 'User', 'Login': None, 'IP': '192.168.137.180', 'MAC': '10-63-c8-9a-7e-cb', 'Port': 10000}]
# {'Type': 'User', 'Login': None, 'IP': '192.168.137.180', 'MAC': '10-63-c8-9a-7e-cb', 'Port': 10000}

def make_open_chat(list_Other_users):
    # global gl_list_Other_users

    dict_connections = {}
    
    str_input_command = ''
    
    while str_input_command != '-с':
        for i in range(len(gl_list_Other_users)): 
            print(i+1, gl_list_Other_users[i])
            
        # print(list(dict_connections))
        
        for i in range(len(list(dict_connections))): 
            print(i+1, ( dict_connections[list(dict_connections)[i]].print_listener_info() ) )
        
        
        str_input_command = str(input('Введете указание : '))
        # соедини с -192.168.137.180  #соедини с -192.168.232.30
        if re.search('соедини с -', str_input_command):
            str_IP_to_connect = (str_input_command.split('-')[1])
            
            # make_connection_and_listen(str_IP_to_connect, 10000)
            
            dict_connections[str_IP_to_connect] = listener(str_IP_to_connect, 10000)
            
        # напиши -192.168.137.180
        elif re.search('напиши -', str_input_command):
            str_IP_to_write = (str_input_command.split('-')[1])
            dict_connections[str_IP_to_write].write_to()
        
        # закрой соединение с -192.168.137.180
        elif re.search('закрой соединение с -', str_input_command):
            str_IP_to_terminate = (str_input_command.split('-')[1])
            dict_connections[str_IP_to_terminate].kill_listener()
            
    for i in range(len(list(dict_connections))):
        dict_connections[list(dict_connections)[i]].kill_listener()
        # print("Соединение с ", list(dict_connections)[i] , "закрыто." )
        
            
    sys.exit()
        
make_open_chat(gl_list_Other_users)