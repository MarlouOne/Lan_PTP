# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 18:19:16 2022

@author: kp587
"""

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('192.168.137.1', 10000))

server_address = ('192.168.137.180', 10000)##############################

sock.connect_ex(server_address)

data = ''

while data != '-q':
    data = input('msg => ').encode()
    sock.sendall(data)

sock.close()

input('enter for quit')