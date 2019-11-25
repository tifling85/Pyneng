# -*- coding: utf-8 -*-

'''
Задание 26.1a

В этом задании надо сделать так, чтобы экземпляры класса Topology были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 25.1x или задания 26.1.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
'''
import pprint

topology_example = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
                    ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
                    ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
                    ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
                    ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
                    ('R3', 'Eth0/2'): ('R5', 'Eth0/0'),
                    ('SW1', 'Eth0/1'): ('R1', 'Eth0/0'),
                    ('SW1', 'Eth0/2'): ('R2', 'Eth0/0'),
                    ('SW1', 'Eth0/3'): ('R3', 'Eth0/0')}

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
            
    def __add__(self, other):
        new_top = {**self.topology, **other.topology}
        return Topology(new_top)
    
    def __iter__(self):
        return iter(tuple(self.topology.items()))


if __name__ == '__main__':
    top = Topology(topology_example)
    for i in top:
        print(i)
    

