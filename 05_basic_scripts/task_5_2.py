# -*- coding: utf-8 -*-
'''
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''
network = input('Input IP network, pls: ')
ip =[int(i) for i in network.split('/')[0].split('.')]
maskpr = '/' +  network.split('/')[1]
mask = int(network.split('/')[1])
mask_bin = mask*'1' + (32-mask)*'0'
mask_bin = [mask_bin[i:i+8] for i in range(0,len(mask_bin),8) ]
mask_int = [int(i,2) for i in mask_bin]

template_addr = '''Network:
{0:<8} {1:<8} {2:<8} {3:<8}
{0:08b} {1:08b} {2:08b} {3:08b}
'''
template_mask = '''Mask:
{0}
{1:<8} {2:<8} {3:<8} {4:<8}
{1:<08b} {2:<08b} {3:<08b} {4:<08b}
'''
print(template_addr.format(ip[0], ip[1], ip[2], ip[3]))
print(template_mask.format(maskpr, mask_int[0], mask_int[1], mask_int[2], mask_int[3]))


