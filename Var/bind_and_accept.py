# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 18:04:07 2022

@author: kp587
"""

import socket



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.137.1', 10000)##############################

sock.bind(server_address)
sock.listen(1)
print('wait......')
connection, client_addr = sock.accept()
print(client_addr)
print(type(connection))
print(f'connect with => {client_addr}')

flag = True
while flag == True:
    data = connection.recv(1024).decode()
    
    if data:
        print(f'rcv => {data}')
        if data == '-q':
            connection.close()
            sock.close()
            input('enter fo quit')
            break
    else:
        continue
    

    


