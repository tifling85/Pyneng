# -*- coding: utf-8 -*-
'''
Задание 22.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
'''

import textfsm, pprint, netmiko, yaml, logging, itertools
from textfsm import clitable
from concurrent.futures import ThreadPoolExecutor

def send_and_parse_show_command(device_dict, command, templates_path):
    logging.info(f'Connecting to {device_dict["ip"]}...')
    with netmiko.ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        command_output = ssh.send_command(command)
        print(command_output)
    cli_table = clitable.CliTable('index', templates_path)
    attributes_dict = {'Command':command}
    cli_table.ParseCmd(command_output, attributes_dict)
    res_lst =  [list(row) for row in cli_table]
    header_lst = list(cli_table.header)
    return [(dict(zip(header_lst, fsm_el))) for fsm_el in res_lst]


if __name__ == '__main__':
    logging.basicConfig(format = '%(threadName)s %(message)s',
                        level=logging.INFO)
    with open ('devices.yaml') as f:
        devices_dict = yaml.load(f, Loader = yaml.FullLoader)
    with ThreadPoolExecutor(max_workers=10) as executor:
        f_result = executor.map(send_and_parse_show_command, devices_dict, itertools.repeat('sh ip int br'), itertools.repeat('templates'))
        pprint.pprint(list(f_result))


