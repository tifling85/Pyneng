# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

template = '''
Protocol:           {}
Prefix:             {}
AD/Metric:          {}
Next-Hop:           {}
Last update:        {}
Outbound Interface: {}
'''

with open('ospf.txt') as f:
    for line in f:
        data = [i.strip('[],') for i in line.split()]
        if data[0] == 'O': data[0] = 'OSPF'
        print(template.format(data[0], data[1], data[2], data[4], data[5], data[6]))

