# -*- coding: utf-8 -*-
'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''

import re
from pprint import pprint

def parse_sh_cdp_neighbors(show_cdp):
    res_dict = {}
    regex = r'(?P<devname>\S+)>show|(?P<neigh>\S+) +(?P<l_intf>Eth \S+).+(?P<port_neigh>Eth \S+)'
    matches = re.finditer(regex, show_cdp)
    for match in matches:
        if match.lastgroup == 'devname':
            devname = match.group('devname')
            res_dict[devname] = {}
        elif match.lastgroup == 'port_neigh':
            res_dict[devname][match.group('l_intf')] = {match.group('neigh'):match.group('port_neigh')}
    return res_dict

if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt') as f:
        res_dict = parse_sh_cdp_neighbors(f.read())
        pprint(res_dict)

