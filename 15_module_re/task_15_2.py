# -*- coding: utf-8 -*-
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''

import re, pprint


def parse_sh_ip_int_br(conf_file):
    lst_cnf = []
    with open(conf_file) as f:
        regex = r'(?P<intf>\S+) +(?P<ip>\S+).+(?P<status>up|administratively down) +(?P<prot>\S+)'
        for regiter in re.finditer(regex, f.read()):
            lst_cnf.append((regiter.group('intf'), regiter.group('ip'), regiter.group('status'), regiter.group('prot')))
    return lst_cnf


if __name__ == '__main__':
    pprint.pprint(parse_sh_ip_int_br('sh_ip_int_br.txt'))


