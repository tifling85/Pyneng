# -*- coding: utf-8 -*-
'''
Задание 22.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - templates

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 22.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
'''

import textfsm, pprint 
from textfsm import clitable

def parse_command_dynamic(command_output, attributes_dict, index_file = 'index', templ_path = 'templates'):
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    res_lst =  [list(row) for row in cli_table]
    header_lst = list(cli_table.header)
    return [(dict(zip(header_lst, fsm_el))) for fsm_el in res_lst]



if __name__ == '__main__':
    with open ('output/sh_ip_int_br.txt') as f:
        command_output = f.read()
    attributes_dict = {'Command':'show ip interface brief', 'Vendor':'Cisco'}
    res = parse_command_dynamic(command_output, attributes_dict)
    print(command_output)
    pprint.pprint(res)
