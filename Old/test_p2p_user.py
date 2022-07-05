#test_p2p_user

import socket
import sys
import threading
#import keyboard
import time

# создаемTCP/IP сокет

ip = 'good'
stop = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_for_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Привязываем сокет к порту
    server_address = ('192.168.137.1', 10000)
    print('Старт сервера на {} порт {}'.format(*server_address))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
except OSError:
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
# Слушаем входящие подключения
sock.listen(1)
clients = []

def thread_for_clients():
    global stop
    print('Ожидание соединения...')
    try:
        connection, client_address = sock.accept() #ТУТ ПОЯВЛЯЕТСЯ ОШИБКА С АДРЕСССОМ - 
        # ГЛАВНЫЙ КОД ВЫРУБАЕТ СОКЕТ РАНЬШЕ, ЧЕМ КОНЧАЕТСЯ ЭТОТ ПОТОК Может быть)
    except WindowsError:
        print('error with sock')

    while stop == False:
        # ждем соединения
        
        
        try:
            print('На связи с:', client_address)
            clients.append(client_address[0])
            # Принимаем данные порциями и ретранслируем их
            while stop == False:
                try:
                    data = connection.recv(1024)
                    print(f'Получено: {data.decode()}')
                    if data:
                        connection.sendall('Доставлено'.encode())
                        
                except:
                    continue
                # else:
                #     # connection.sendall(b'Ошибка отправки')
                #     print('Нет данных от:', client_address)
                #     break
        except:
            # Очищаем соединение
            connection.close()
    sock.close()
    sys.exit()
    # sock_for_connect.close()
            
def thread_for_connecting():
    global stop
    global ip
    while stop == False:
        try:
            ip = input('call to :')
            if ip == 'q':
                stop = True
                sys.exit()
            sock_for_connect.connect((ip, 10000))
        
            
            while stop == False:
            
            # print('Подключено к {} порт {}'.format(*server_address))
    
                try:
                # Отправка данных
                    mess = input('you: ')
                    message = mess.encode()
                    sock_for_connect.sendall(message)
            
                # Смотрим ответ
                    answer = sock_for_connect.recv(1024)
                    if answer:
                        print('Доставлено')
                except:
                    print('Закрываем сокет')
                    sock_for_connect.close()
            # finally:
            #     print('Закрываем сокет')
            #     sock_for_connect.close()
        except:
            print('backConnect error')
            
    # sock.close()
    sock_for_connect.close()

def closer():
    sock.close()
    sock_for_connect.close()
    print('sockets are closed, mb')
    sys.exit('press enter for exit')

    
def main():
    global stop
    try:
        thread_listen = threading.Thread(target=thread_for_clients)
        thread_sending = threading.Thread(target=thread_for_connecting)
        thread_closer = threading.Thread(target=closer)

        
        thread_listen.start()
        thread_sending.start()
    except:
        print('ERROR')
        stop = True
        # sock.close()
        sock_for_connect.close()
    while ip != 'q':
        pass
    stop = True
    time.sleep(2)
    thread_closer.start()
    # thread_listen.join()
    # thread_sending.join()
    # sock.close()
    # sock_for_connect.close()
    sys.exit(0)
main()
