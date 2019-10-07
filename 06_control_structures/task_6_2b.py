# -*- coding: utf-8 -*-
'''
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

while True:
    try:
        ip = [int(i) for i in input('Input IP address: ').split('.')]
    except ValueError:
        print('Invalid IP address!')
        continue

    if len(ip) != 4 or not all(octet in range(0,256) for octet in ip):
        print('Invalid IP address!')
        continue
    else:
        if ip[0] > 0 and ip[0] < 224:
            print('Unicast')
        elif ip[0] in range(224, 240):
            print('Multicast')
        elif all(addr==255 for addr in ip):
            print('local broadcast')
        elif all(addr==0 for addr in ip):
            print('unassigned')
        else:
            print('Unused')
    break
