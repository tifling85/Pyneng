# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

import ipaddress, subprocess


def ping_ip_addresses(lst_ip):
    res_tuple = ([],[])
    avail, notavail = res_tuple
    for ip in lst_ip:
        print('check {}'.format(ip))
        reply = subprocess.run(['ping', '-c', '3', ip], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if reply.returncode == 0:
            avail.append(ip)
        else:
            notavail.append(ip)
    return res_tuple


if __name__ == '__main__':
    lst_ip = ['8.8.8.8', '192.168.240.1', '12.12.12.12']
    print(ping_ip_addresses(lst_ip))

