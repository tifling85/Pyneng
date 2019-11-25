# -*- coding: utf-8 -*-

'''
Задание 26.3

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также выполняется проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать исключение ValueError с соответствующим текстом (смотри вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра: ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

'''

import re

class IPAddress:

    def __init__(self, ip):
        ipaddr = ip.split('/')
        if len(ipaddr[0].split('.')) != 4:
            raise ValueError('Incorrect IP address')
        for i in ipaddr[0].split('.'):
            if not i.isdigit():
                raise ValueError('Incorrect IP address')
            if int(i) not in range(0,255):
                raise ValueError('Incorrect IP address')
        if not ipaddr[1].isdigit():
            raise ValueError('Incorrect mask')
        if int(ipaddr[1]) not in range(8,32):
            raise ValueError('Incorrect mask')
        self.ip, self.mask = ipaddr


if __name__ == '__main__':
    ip1 = IPAddress('1.1.1.1/24')
    print(ip1.ip)
    print(ip1.mask)
    ip2 = IPAddress('1.1.1.1/33')

