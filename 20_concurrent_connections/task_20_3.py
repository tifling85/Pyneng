# -*- coding: utf-8 -*-
'''
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging, yaml, netmiko, pprint, itertools

logging.basicConfig(format = '%(threadName)s %(levelname)s: %(message)s',
                    level=logging.INFO)

def send_request(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        logging.info(f'Cheking {device["ip"]}')
        ssh.enable()
        return ssh.find_prompt() + ssh.send_command(command, strip_command = False) + '\n'


def send_command_to_devices(devices, commands_dict, filename, limit = 3):
    lst_futures = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        for device in devices:
            for command in commands:
                if device['ip'] == command:
                    lst_futures.append(executor.submit(send_request,
                                                    device, commands[command]))
    with open(filename, 'w') as f:
        for res in as_completed(lst_futures):
            f.write(res.result())
    
if __name__ == '__main__':
    with open ('devices.yaml') as f:
        devices = yaml.load(f, Loader = yaml.FullLoader)
    commands = {'192.168.100.1': 'sh ip int br',
                '192.168.100.2': 'sh arp',
                '192.168.100.3': 'sh ip int br'}
    filename = 'for_task_20_3.txt'
    send_command_to_devices(devices, commands, filename)


