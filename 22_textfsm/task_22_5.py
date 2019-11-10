# -*- coding: utf-8 -*-
'''
Задание 22.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 22.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
'''
import textfsm, pprint, netmiko, yaml, logging, itertools
from textfsm import clitable
from concurrent.futures import ThreadPoolExecutor

def send_and_parse_show_command(device_dict, command, templates_path):
    logging.info(f'Connecting to {device_dict["ip"]}...')
    with netmiko.ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()[:-1]
        command_output = ssh.send_command(command)
    cli_table = clitable.CliTable('index', templates_path)
    attributes_dict = {'Command':command}
    cli_table.ParseCmd(command_output, attributes_dict)
    res_lst =  [list(row) for row in cli_table]
    header_lst = list(cli_table.header)
    return {prompt:[(dict(zip(header_lst, fsm_el))) for fsm_el in res_lst]}


if __name__ == '__main__':
    logging.basicConfig(format = '%(threadName)s %(message)s',
                        level=logging.INFO)
    with open ('devices.yaml') as f:
        devices_dict = yaml.load(f, Loader = yaml.FullLoader)
    with ThreadPoolExecutor(max_workers=10) as executor:
        f_result = executor.map(send_and_parse_show_command, devices_dict, itertools.repeat('sh ip int br'), itertools.repeat('templates'))
        pprint.pprint(list(f_result))

