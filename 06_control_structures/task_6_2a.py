# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
try:
    ip = [int(i) for i in input('Input IP address: ').split('.')]
except ValueError:
    print('Invalid IP address!')
else:    
    if len(ip) != 4 or not all(octet in range(0,256) for octet in ip):
        print('Invalid IP address!')
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


