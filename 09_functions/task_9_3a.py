# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
def get_int_vlan_map(cfg_in):
    tup_out = ({},{})
    access, trunk = tup_out
    with open(cfg_in) as f:
        for line in f:
            if 'interface' in line:
                intf = line.split()[-1]
            if 'mode access' in line:
                mode = 'access'
            elif 'trunk encapsulation' in line:
                mode = 'trunk'
            if 'vlan' in line and mode == 'access':
                access[intf] = line.split()[-1]
            elif 'vlan' in line and mode == 'trunk':
                trunk[intf] = line.split()[-1].split(',')
            if 'duplex auto' in line and mode == 'access' and not access.get(intf):
                access[intf] = 1
    return tup_out

tup_out = get_int_vlan_map('config_sw2.txt')
for el in tup_out:
    print(el)
