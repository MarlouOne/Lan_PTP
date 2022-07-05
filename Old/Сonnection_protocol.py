# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:18:54 2022

@author: Marlou
"""

import socket
import sys
import os

def get_self_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def make_new_connects(str_server_IP, int_server_port):
    sock_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_connect.connect(str_server_IP,int_server_port)
    return sock_connect

def server_part():
    
    
# # test-server.py
# import socket
# import sys

# def getMyIp():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
#     s.connect(('<broadcast>', 0))
#     return s.getsockname()[0]

# # создаемTCP/IP сокет
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Привязываем сокет к порту
# server_address = (getMyIp(), 10000)
# print('Старт сервера на {} порт {}'.format(*server_address))
# sock.bind(server_address)

# # Слушаем входящие подключения
# sock.listen(1)

# while True:
#     # ждем соединения
#     print('Ожидание соединения...')
#     connection, client_address = sock.accept()
#     try:
#         print('Подключено к:', client_address)
#         # Принимаем данные порциями и ретранслируем их
#         while True:
#             data = connection.recv(16)
#             print(f'Получено: {data.decode()}')
#             if data:
#                 print('Обработка данных...')
#                 data = data.upper()
#                 print('Отправка обратно клиенту.')
#                 connection.sendall(data)
#             else:
#                 print('Нет данных от:', client_address)
#                 break

#     finally:
#         # Очищаем соединение
#         connection.close()

# # test-client.py
# import socket
# import sys
# import os

# # def get_ip_serv():
# #     response_art = os.popen('arp -a')
# #     data_arp = response_art.readlines()
# #     for line_arp in data_arp:
# #         flag = line_arp.split()
# #         if len(flag) > 0 and flag[0][-1] == '1' and flag[0][-2] == '.':
# #             tmp = flag[0]
# #             print('Ip of serv:', tmp)
# #     return tmp

# # СоздаемTCP/IP сокет
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Подключаем сокет к порту, через который прослушивается сервер
# server_address = ('192.168.137.180', 10000)
# print('Подключено к {} порт {}'.format(*server_address))
# sock.connect(server_address)

# try:
#     # Отправка данных
#     mess = 'Hello Wоrld!'
#     print(f'Отправка: {mess}')
#     message = mess.encode()
#     sock.sendall(message)
    
#     # Смотрим ответ
#     amount_received = 0
#     amount_expected = len(message)
#     while amount_received < amount_expected:
#         data = sock.recv(16)
#         amount_received += len(data)
#         mess = data.decode()
#         print(f'Получено: {data.decode()}')

# finally:
#     print('Закрываем сокет')
#     sock.close()
