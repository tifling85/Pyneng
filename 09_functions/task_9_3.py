# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(cfg_in):
    tup_out = ({},{})
    access, trunk = tup_out
    with open(cfg_in) as f:
        for line in f:
            if 'interface' in line:
                intf = line.split()[-1]
            if 'mode access' in line:
                mode = 'access'
            elif 'trunk encapsulation' in line:
                mode = 'trunk'
            if 'vlan' in line and mode == 'access':
                access[intf] = line.split()[-1]
            elif 'vlan' in line and mode == 'trunk':
                trunk[intf] = line.split()[-1].split(',')
    return tup_out

tup_out = get_int_vlan_map('config_sw1.txt')
for el in tup_out:
    print(el)

