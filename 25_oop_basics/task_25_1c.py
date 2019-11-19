# -*- coding: utf-8 -*-

'''
Задание 25.1c

Изменить класс Topology из задания 25.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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
    top.delete_node('SW4')
    pprint.pprint(top.topology)
