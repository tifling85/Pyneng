# -*- coding: utf-8 -*-

'''
Задание 26.3a

Изменить класс IPAddress из задания 26.3.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

Для этого задания нет теста!
'''

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

    def __str__(self):
        return 'IP Address {}/{}'.format(self.ip, self.mask)
    
    def __repr__(self):
        return "IPAddress('{}/{}')".format(self.ip, self.mask)

if __name__ == '__main__':
    ip1 = IPAddress('1.1.1.1/24')
    print(ip1)
    lst = []
    lst.append(ip1)
    print(lst)
