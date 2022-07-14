# -*- coding: utf-8 -*-
"""
Created on Sun May  1 17:19:05 2022

@author: kp587
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:09:38 2022

@author: kp587
"""

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 192.168.147.30 sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_address = ('192.168.42.129', 10000)##############################

sock.bind(server_address)
sock.listen(1)
print('wait......')
connection, client_addr = sock.accept()
print(f'connect with => {client_addr}')

data = ' '

def recive_file():
    head = connection.recv(1024).decode().split(',')#ждёт получение головы
    print(head)#
    size = int(head[1])#забирает размер из головы
    format_of_file = str(head[0])#забирает формат файла
    print(size, format_of_file)#
    data = b''
    for i in range(0, (size//1024) + 1):
        
        data += connection.recv(1024)# получает файл, выделяя буфер размера size
        connection.send('fin'.encode())
        # print(f'packet number {i+1}')
    # if data != '-f':
        # connection.sendall('fin'.encode())#отправляет флаг успешного получения 'fin'
    file = open(f'RcvFile.{format_of_file}', 'wb')#записывает побайтно файл необходимого расширения
    file.write(data)#
    file.close()#
    data = 'Файл получен'#
    # else:
        # connection.sendall('err'.encode())#отправляет флаг пиздеца
        # data = 'Ошибка получения'#
    # print(data.decode())
    
    
    return data#
    # connection.close()
    # sock.close()
    # data = '-q'
    # file.close()
            # break
    
flag = True
while flag == True:
    data = connection.recv(1024).decode()
    if data:
        if data == '-f':
            data = recive_file()
        print(f'rcv => {data}')
        if data == '-q':
            
            sock.close()
            connection.close()
            input('enter fo quit')
            break
    else:
        continue
    

    


