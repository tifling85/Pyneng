# -*- coding: utf-8 -*-
'''
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
'''
from concurrent.futures import ThreadPoolExecutor
import logging, yaml, netmiko, pprint, itertools

logging.basicConfig(format = '%(threadName)s %(levelname)s: %(message)s',level=logging.INFO)

def send_request(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        logging.info(f'Cheking {device["ip"]}')
        ssh.enable()
        return ssh.find_prompt() + ssh.send_command(command, strip_command = False) + '\n'

def send_show_command_to_devices(devices, command, filename = None, limit=3):
    with ThreadPoolExecutor(max_workers = limit) as executor:
        res_iter = executor.map(send_request, devices, itertools.repeat(command))
    with open(filename, 'w') as f:
        for res in res_iter:
            f.write(res)
    

if __name__ == '__main__':
    with open ('devices.yaml') as f:
        devices = yaml.load(f, Loader = yaml.FullLoader)
    command = 'sh ip int br'
    filename = 'for_task_20_2.txt'
    send_show_command_to_devices(devices, command, filename = 'for_task_20_2.txt')


