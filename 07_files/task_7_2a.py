# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']
import sys

with open(sys.argv[1]) as f:
    for line in f:
        flag_ign = False
        for ign in ignore:
            if ign in line:
                #print(ign)
                flag_ign = True
                break

        if not line.startswith('!') and flag_ign == False:
            print(line, end = '')
            

