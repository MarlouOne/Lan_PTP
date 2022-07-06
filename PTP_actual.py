
"""
@author: Marlou
"""

"""
https://russianblogs.com/article/5838278912/ <- Запуск кода от имени администратора
"""

"""
netsh wlan set hostednetwork mode=allow ssid="ИМЯ_СЕТИ" key="ПОРОЛЬ_8_СИМВОЛОВ" <- Создание беспроводной сети
netsh wlan set hostednetwork mode=allow ssid="test_Network" key="12345678"
netsh wlan start hostednetwork <- Запуск беспроводной сети
netsh wlan set hostednetwork mode=disallow <- Для точного запуска сети 1-ая команда
netsh wlan set hostednetwork mode=allow <- Для точного запуска сети 2-ая команда

netsh wlan stop hostednetwork <– останавливает раздачу Wi-Fi
netsh wlan show settings <– выводит информацию о сети и отображает ее состояние.
NETSH WLAN show hostednetwork
netsh wlan connect name=ИмяПрофиляСети <- Для подключения к WiFi сети служит команда

netsh interface show interface
CLS <- очистка консоли windows
"""
"""
netstat -na|find "10000"
netsh wlan show driver
netsh wlan show interface
arp -a
ipconfig /displaydns
ipconfig /all
ipconfig
getmac
netsh interface show interface
netsh wlan show networks <- Отображает доступные подключения по wifi
"""

# from __future__ import print_function
import ctypes, sys
import subprocess
import os


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def do_command(list_commands):
    if is_admin(): # Добавьте код для запуска здесь
        for i in range(len(list_commands)):
            subprocess.run(list_commands[i], shell=True)
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

class connection():
    str_name : str
    str_ip : str
    str_mac : str

    def get_self_ip(self):
        str_netDriver = os.popen('netsh wlan show driver').readlines()[3].split(':')[1][1:]
        print("Net driver - ", str_netDriver)
        response = os.popen('netsh wlan show interface')
        data = response.readlines()
        # print(data)
        print('2222')

#   response = os.popen(comm)
#   data = response.readlines()

    def __init__(self):
        self.get_self_ip()



def main() -> None:
    list_commands = ['netsh interface show interface']
    connection()
    do_command(list_commands)



    input("Press any key...")




main()