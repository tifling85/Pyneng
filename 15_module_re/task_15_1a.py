# -*- coding: utf-8 -*-
'''
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

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
                res_dict[intf] = (iterreg.group('ipadr'), iterreg.group('port'))
    return res_dict


if __name__ == '__main__':
    res_dict = get_ip_from_cfg('config_r1.txt')
    pprint.pprint(res_dict)
