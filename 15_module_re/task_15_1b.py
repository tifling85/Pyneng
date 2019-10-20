# -*- coding: utf-8 -*-
'''
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом, чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re
import pprint

def get_ip_from_cfg(cfg_name):
    res_dict = {}
    regex = (r'interface (?P<intf>\S+)|ip address (?P<ipad>(?P<ipadr>\S+) (?P<port>\S+))')
    with open(cfg_name) as f:
        for iterreg in re.finditer(regex, f.read()):
            if iterreg.lastgroup == 'intf':
                intf = iterreg.group('intf')
            if iterreg.lastgroup == 'ipad':
                if not res_dict.get(intf):
                    res_dict[intf] = [(iterreg.group('ipadr'), iterreg.group('port'))]
                else:
                    res_dict[intf].append((iterreg.group('ipadr'), iterreg.group('port')))
    return res_dict


if __name__ == '__main__':
    res_dict = get_ip_from_cfg('config_r2.txt')
    pprint.pprint(res_dict)
