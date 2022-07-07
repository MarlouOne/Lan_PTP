from codecs import ignore_errors
import os



str_netDriver = os.popen('netsh wlan show driver').readlines()[3].split(':')[1][1:]
print("Net driver - ", str_netDriver)
response = os.popen('netsh wlan show interface').read()

print(type(response))
# data = response.readlines()
# # print(data)
# print('2222')
