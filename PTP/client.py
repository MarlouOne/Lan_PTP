import socket
import json
import threading
import time
from colorama import init
from colorama import Fore

def jsonBuilder(str):
    return json.dumps(str)

def request(content):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 15000))
    sock.send(bytes(content,'utf-8'))
    response = sock.recv((1024))
    result = response.decode()
    sock.close()
    return  result

def connection(user_name):
    content = jsonBuilder(({'user_name': user_name}))
    print(request(content))

def send_message(_for,user_name,text):
    content = jsonBuilder(({'for':_for,"text":user_name + ":" + text}))
    print(request(content))

def get_massage(user_name):
    while True:
        content = jsonBuilder(({'get': user_name}))
        result = request(content)
        if result != "":
            print()
            print(" %45s "%(Fore.GREEN + result + Fore.RESET))
        time.sleep(5)

init()

user_name = input('Введите ваш логин : ')
connection(user_name)

thread = threading.Thread(target=get_massage, args=[user_name])
thread.start()

while True:
    _for = input('Кому написать сообщение: ')
    _text = input("Текст сообщеня: ")
    send_message(_for, user_name, _text)