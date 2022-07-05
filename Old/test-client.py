# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:46:42 2022

@author: Marlou
"""

# test-client.py
import socket
import sys
import os

# def get_ip_serv():
#     response_art = os.popen('arp -a')
#     data_arp = response_art.readlines()
#     for line_arp in data_arp:
#         flag = line_arp.split()
#         if len(flag) > 0 and flag[0][-1] == '1' and flag[0][-2] == '.':
#             tmp = flag[0]
#             print('Ip of serv:', tmp)
#     return tmp

# СоздаемTCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаем сокет к порту, через который прослушивается сервер
server_address = ('192.168.137.180', 10000)
print('Подключено к {} порт {}'.format(*server_address))
sock.connect(server_address)

try:
    # Отправка данных
    mess = 'Hello Wоrld!'
    print(f'Отправка: {mess}')
    message = mess.encode()
    sock.sendall(message)
    
    # Смотрим ответ
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        mess = data.decode()
        print(f'Получено: {data.decode()}')

finally:
    print('Закрываем сокет')
    sock.close()