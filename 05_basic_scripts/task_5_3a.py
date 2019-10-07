# -*- coding: utf-8 -*-
'''
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
'''

access_template = [ 'input number of vlan: ',
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [ 'input allowed vlans: ',
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]

dict_temp = {'access' : access_template, 'trunk':trunk_template}

mode = input('input mode interface: ')
num_if = input('input type and number interface: ')
num_vlan = input(dict_temp[mode].pop(0))

print('interface {}'.format(num_if))
print('\n'.join(dict_temp[mode]).format(num_vlan))


