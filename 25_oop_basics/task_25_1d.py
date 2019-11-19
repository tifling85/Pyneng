# -*- coding: utf-8 -*-

'''
Задание 25.1d

Изменить класс Topology из задания 25.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


'''

import pprint

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology):
        edit_lst = []
        for i,j in topology.items():
            for j_rev, i_rev in topology.items():
                if i==i_rev and j==j_rev:
                    if i_rev not in edit_lst: edit_lst.append(j_rev) 
        for i in edit_lst:
            del topology[i]
        return topology

    def delete_link(self, item):
        del_item = False
        for i,j in self.topology.items():
            if item[0] == i and item[1] == j:
                del self.topology[i]
                del_item = True
                break
            elif item[1] == i and item[0] == j:
                del_item = True
                del self.topology[i]
                break
        if del_item == False:
            print('Such connection is not found!')

    def delete_node(self, item):
        edit_lst = []
        for i,j in self.topology.items():
            if item in i or item in j:
                edit_lst.append(i)
        for i in edit_lst:
            del self.topology[i]
        if not edit_lst: print('Not such device!!!')

    def add_link(self, item1, item2):
        exists = False
        for i,j in self.topology.items():
            if (i == item1 and j == item2) or (i == item2 and j == item1):
                print('Such connect is exist!')
                exists = True
                break
            elif i == item1 or i == item2 or j == item1 or j == item2:
                print('Connect with port is exist')
                exists = True
                break
        if exists == False:
            self.topology[item1] = item2

topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}

if __name__ == '__main__':
    top = Topology(topology_example)
    pprint.pprint(top.topology)
    top.add_link(('R5', 'Eth0/4'), ('SW1', 'Eth0/6'))
    pprint.pprint(top.topology)
