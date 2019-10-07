# -*- coding: utf-8 -*-
'''
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить тип IP-адреса.
3. В зависимости от типа адреса, вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
ip = [int(i) for i in input('Input IP address: ').split('.')]
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



