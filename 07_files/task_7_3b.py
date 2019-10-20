# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
vlan = int(input('Input VLAN, pls: '))

template = '{:4}  {}  {:7}'
data_lst = []
with open('CAM_table.txt') as f:
    for line in f:
        line = line.split()
        if len(line) != 4 or not line[0].isdigit():
            continue
        data_lst.append([int(line[0]), line[1], line[3]])
    data_lst.sort()
    for line in data_lst:
        if line[0] == vlan:
            print(template.format(line[0], line[1], line[2]))
