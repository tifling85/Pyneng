# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']
import sys

with open(sys.argv[1]) as f, open('config_sw1_cleared.txt', 'w') as f_out:
    for line in f:
        flag_ign = False
        for ign in ignore:
            if ign in line:
                flag_ign = True
                break

        if flag_ign == False:
            f_out.write(line)
