# -*- coding: utf-8 -*-
'''
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
import sys

network = sys.argv[1]
ip =[int(i) for i in network.split('/')[0].split('.')]
maskpr = '/' +  network.split('/')[1]
mask = int(network.split('/')[1])
mask_bin_str = mask*'1' + (32-mask)*'0'
ip_bin_str = '{:08b}'.format(ip[0]) + '{:08b}'.format(ip[1]) + '{:08b}'.format(ip[2]) + '{:08b}'.format(ip[3])
network_bin_str =bin(int(mask_bin_str,2)&int(ip_bin_str,2))[2:]
network_bin_lst = [network_bin_str[i:i+8] for i in range(0,len(network_bin_str),8) ]
network_int = [int(i,2) for i in network_bin_lst]
mask_bin_lst = [mask_bin_str[i:i+8] for i in range(0,len(mask_bin_str),8) ]
mask_int = [int(i,2) for i in mask_bin_lst]

template_net = '''Network:
{0:<8} {1:<8} {2:<8} {3:<8}
{0:08b} {1:08b} {2:08b} {3:08b}
'''
template_mask = '''Mask:
{0}
{1:<8} {2:<8} {3:<8} {4:<8}
{1:<08b} {2:<08b} {3:<08b} {4:<08b}
'''
print(template_net.format(network_int[0], network_int[1], network_int[2], network_int[3]))
print(template_mask.format(maskpr, mask_int[0], mask_int[1], mask_int[2], mask_int[3]))

