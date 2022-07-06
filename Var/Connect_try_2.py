# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:09:16 2022

@author: dadpavlo
"""

from threading import Thread, Event
import socket
import sys

import re

def get_self_ip():
    # self_ip = '192.168.137.1' # 192.168.0.6
    self_ip = '192.168.0.6'
    return self_ip
   


class client():
    gl_dict_clients = {}
        
    str_ip : str
    int_port : int
    sock : socket
   
    def info(self):
        print(f'{self.str_ip} - {self.int_port}')
    
    def __init__(self, str_IP_to_connect, int_port_to_connect, int_mode=1, connected_socket=''):
        if int_mode == 1:
            self.str_ip = str_IP_to_connect
            self.int_port = int_port_to_connect
            thread_call = Thread(target=self.th_call_to_client, args=(), daemon=False)
            thread_call.start()

        elif int_mode == 2:
            self.str_ip = str_IP_to_connect
            self.int_port = int_port_to_connect
            self.sock = connected_socket
            client.gl_dict_clients[self.str_ip] = self
    
    def write_to(self):
        str_data = ''
        while str_data != '-c': # минус с (на РУССКОМ)
            str_data = input(f"Write to {self.str_ip} on {self.int_port}: ")
            self.sock.sendall(str_data.encode())
            
    def th_reception_messages(self):
        while flag == True:
            str_content = self.sock.recv(1024).decode()
            
            if str_content:
                print(f'Message from {self.str_ip}: {str_content}')
                if str_content == '-с':
                    self.sock.close()
                    print(f" User {self.str_ip} break the connection.")
                    break
            else:
                continue
        
        
    
    def th_call_to_client(self):
        print('Start colling...')
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        bool_connection_stat = False
        int_try_counter = 0
        
        print(f'Calling to {self.str_ip} on {self.int_port}...')
        
        while bool_connection_stat == False or int_try_counter != 4:

            try:
                
                sock.connect( (self.str_ip, self.int_port) )
                self.sock = sock
                bool_connection_stat = True


                client.gl_dict_clients[self.str_ip] = self
                print(f'Connected to {self.str_ip} on {self.int_port}.')
                
                sock.close()
                sys.exit()
                
            except Exception:
                # print('pass')
                continue
        
        print(f'Timeout to {self.str_ip} on {self.int_port}.')
        
        sock.close()
        sys.exit()



class listener():
    bool_flag_to_listen = True
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
        bool_connection_stat = False    

        while bool_connection_stat == False:
            try:
                print('Ready for get connection.')
                new_socket, list_client_info = sock.accept()
                bool_connection_stat = True
                print(f'Connected with {list_client_info[0]} by port {list_client_info[1]}')
                      
                client.gl_dict_clients[list_client_info[0]] = client(list_client_info[0], list_client_info[1], 2, new_socket)
                sock.close()
                
                thread_listening = Thread(target=self.eternal_listen, args = (), daemon=False)
                thread_listening.start()
                
            except Exception:
                # print('error')
                continue
            
        sys.exit()

def make_open_chat():

    # str_input_command = ''
    
    listener()

    str_input_command = ''

    while str_input_command != '-с':
        for i in range(  len( list(client.gl_dict_clients) )  ):
            print(i+1, '. ',  client.gl_dict_clients[ list(client.gl_dict_clients)[i] ].info, sep='')
        
        
        str_input_command = str(input('Введете указание : '))
        # соедини с -192.168.137.180  #соедини с -192.168.232.30
        if re.search('соедини с -', str_input_command):
            str_IP_to_connect = (str_input_command.split('-')[1])
            client(str_IP_to_connect, 10000)

            
        # напиши -192.168.137.180
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

make_open_chat()
