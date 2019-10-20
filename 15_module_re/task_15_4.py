# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''
import re


def get_ints_without_description(cfg_file):
    lst_intf = []
    with open(cfg_file) as f:
        regex = r'^interface (?P<intf>\S+)|^ (?P<desc>description)'
        for string in f:
            match = re.search(regex, string)
            if match:
                if match.lastgroup == 'intf':
                    print('add ', match.group('intf'))
                    lst_intf.append(match.group('intf'))
                elif match.lastgroup == 'desc':
                    print('del ', lst_intf.pop())
    return lst_intf


if __name__ == '__main__':
    print(get_ints_without_description('config_r1.txt'))


